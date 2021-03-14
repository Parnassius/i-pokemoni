from __future__ import annotations

from collections.abc import Callable, Mapping
from os.path import join
from typing import Generic, Type, TypeVar, cast

import lz4.block  # type: ignore

from utils import hash_fnv1a_64, read_as_int


class GFPack:
    MAGIC = 0x4B434150_584C4647  # GFLXPACK

    def __init__(self, path: str) -> None:
        with open(path, "rb") as f:
            self.header = GFPackHeader(f.read(GFPackHeader.SIZE))
            self.pointers = GFPackPointers(
                f.read(0x10 + (self.header.count_folders * 8))
            )

            self.hash_absolute = [
                FileHashAbsolute(f.read(FileHashAbsolute.SIZE))
                for _ in range(self.header.count_files)
            ]

            self.hash_in_folder = []
            for i in range(self.header.count_folders):
                table = FileHashFolder(f.read(FileHashIndex.SIZE))
                table.files = [
                    FileHashIndex(f.read(FileHashIndex.SIZE))
                    for _ in range(table.folder.file_count)
                ]
                self.hash_in_folder.append(table)

            self.file_table = [
                FileData(f.read(FileData.SIZE)) for _ in range(self.header.count_files)
            ]

            self.compressed_files = []
            for i in range(self.header.count_files):
                f.seek(self.file_table[i].offset_packed)
                self.compressed_files.append(f.read(self.file_table[i].size_compressed))

            self.decompressed_files = [
                self._decompress(
                    self.compressed_files[i],
                    self.file_table[i].size_decompressed,
                    self.file_table[i].type,
                )
                for i in range(self.header.count_files)
            ]

    @property
    def count(self) -> int:
        return self.header.count_files

    """public byte[] this[int index]
    {
        get => (byte[])DecompressedFiles[index].Clone();
        set
        {
            Modified |= !DecompressedFiles[index].SequenceEqual(value);
            DecompressedFiles[index] = value;
        }
    }"""

    def get_index_file_name(self, name: str) -> int:
        for f in self.hash_in_folder:
            index = f.get_index_file_name(name)
            if index >= 0:
                return f.files[index].index
        return -1

    def get_data_file_name(self, name: str) -> bytes:
        index = self.get_index_file_name(name)
        return self.decompressed_files[index]

    def _decompress(
        self, data: bytes, size_decompressed: int, compression_type: int
    ) -> bytes:
        if compression_type == 1:  # Zlib
            raise Exception  # not implemented
        elif compression_type == 2:  # Lz4
            data = lz4.block.decompress(data, size_decompressed)
        return data

    """public Task<byte[][]> GetFiles() => Task.FromResult(DecompressedFiles);
    public Task<byte[]> GetFile(int file, int subFile = 0) => Task.FromResult(this[file]);"""


class GFPackHeader:
    SIZE = 0x18
    MAGIC = GFPack.MAGIC
    VERSION = 0x1000

    def __init__(self, data: bytes) -> None:
        self.is_relocated = read_as_int(4, data, 0x06)
        self.count_files = read_as_int(4, data, 0x10, True)
        self.count_folders = read_as_int(4, data, 0x14, True)


class GFPackPointers:
    def __init__(self, data: bytes) -> None:
        self.ptr_file_table = read_as_int(8, data, 0x00, True)
        self.ptr_hash_paths = read_as_int(8, data, 0x08, True)
        self.ptr_hash_folders = []
        pos = 0x10
        while pos < len(data):
            self.ptr_hash_folders.append(read_as_int(8, data, pos, True))
            pos += 0x08


class FileHashAbsolute:
    SIZE = 0x08

    def __init__(self, data: bytes) -> None:
        self.hash_fnv1a_path_full = read_as_int(8, data, 0x00)


class FileHashFolder:
    def __init__(self, data: bytes) -> None:
        self.folder = FileHashFolderInfo(data)
        self.files: list[FileHashIndex] = []

    def get_index_file_name(self, name: str) -> int:
        return next((k for k, v in enumerate(self.files) if v.is_match(name)), -1)


class FileHashFolderInfo:
    SIZE = 0x10

    def __init__(self, data: bytes) -> None:
        self.hash_fnv1a_path_folder_name = read_as_int(8, data, 0x00)
        self.file_count = read_as_int(4, data, 0x08, True)
        self.padding = 0xCC

    def is_match(self, name: str) -> bool:
        return hash_fnv1a_64(name) == self.hash_fnv1a_path_folder_name


class FileHashIndex:
    SIZE = 0x10

    def __init__(self, data: bytes) -> None:
        self.hash_fnv1a_path_file_name = read_as_int(8, data, 0x00)
        self.index = read_as_int(4, data, 0x08, True)
        self.padding = 0xCC

    def is_match(self, name: str) -> bool:
        return hash_fnv1a_64(name) == self.hash_fnv1a_path_file_name


class FileData:
    SIZE = 0x18

    def __init__(self, data: bytes) -> None:
        self.level = 9  # quality?
        self.type = read_as_int(2, data, 0x02)
        self.size_decompressed = read_as_int(4, data, 0x04, True)
        self.size_compressed = read_as_int(4, data, 0x08, True)
        self.padding = 0xCC
        self.offset_packed = read_as_int(4, data, 0x10, True)
        self.unused = read_as_int(4, data, 0x14)
