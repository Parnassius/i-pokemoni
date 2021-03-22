from __future__ import annotations

from typing import BinaryIO

from utils import read_as_int

from .large_container import LargeContainer, LargeContainerEntry


class GARC(LargeContainer):
    def __init__(self, path: str) -> None:
        with open(path, "rb") as f:
            self._data = f.read()
            f.seek(0)
            self._header = GARCHeader(f)
            self._FATO = FATO(f)
            self._FATB = FATB(f, self._header.data_offset)
            self.file_count = self._FATO.entry_count

    def _get_file_offset(self, index: int, sub_file: int = 0) -> int:
        f = self._FATB.entries[index].sub_entries[sub_file]
        return f.start

    def get_entry(self, index: int, sub_file: int) -> bytes:
        f = self._FATB.entries[index].sub_entries[sub_file]
        return f.get_file_data(self._data)


class GARCHeader:
    _VER_4 = 0x0400
    _VER_6 = 0x0600

    # public bool VER6 => Version == VER_6;
    # public bool VER4 => Version == VER_4;

    def __init__(self, f: BinaryIO):
        self._magic = read_as_int(4, f)
        self._header_size = read_as_int(4, f, signed=True)
        self._endianess = read_as_int(2, f)
        self._version = read_as_int(2, f)
        self._chunk_count = read_as_int(4, f)

        if self._chunk_count != 4:
            raise Exception(f"Invalid GARC Chunk Count: {self._chunk_count}")

        self.data_offset = read_as_int(4, f, signed=True)
        self.file_size = read_as_int(4, f)

        self.content_largest_padded: int  # Format 6 Only
        self.content_largest_unpadded: int
        self.content_pad_to_nearest: int  # Format 6 Only (4 bytes is standard in VER_4, and is not stored)

        if self._version == self._VER_4:
            self.content_largest_unpadded = read_as_int(4, f, signed=True)
            self.content_pad_to_nearest = 4
        elif self._version == self._VER_6:
            self.content_largest_padded = read_as_int(4, f, signed=True)
            self.content_largest_unpadded = read_as_int(4, f, signed=True)
            self.content_pad_to_nearest = read_as_int(4, f, signed=True)
        else:
            raise Exception(f"Invalid GARC Version: {self._version}")


class FATO:
    def __init__(self, f: BinaryIO) -> None:
        self._magic = read_as_int(4, f)
        self._header_size = read_as_int(4, f, signed=True)
        self.entry_count = read_as_int(2, f)
        self._padding = read_as_int(2, f, signed=True)

        self.entries = []
        for i in range(self.entry_count):
            self.entries.append(FATOEntry(f))


class FATOEntry:
    def __init__(self, f: BinaryIO) -> None:
        self.offset = read_as_int(4, f)


class FATB:
    def __init__(self, f: BinaryIO, data_offset: int) -> None:
        self._magic = read_as_int(4, f)
        self._header_size = read_as_int(4, f, signed=True)
        self._entry_count = read_as_int(2, f)
        self._padding = read_as_int(2, f, signed=True)

        self.entries = []
        for i in range(self._entry_count):
            self.entries.append(FATBEntry(f, data_offset))


class FATBEntry:
    def __init__(self, f: BinaryIO, data_offset: int) -> None:
        self._vector = read_as_int(4, f)

        self.sub_entries = []
        for i in range(32):
            self.sub_entries.append(FATBSubEntry(f, data_offset, i, self._vector))
        self.is_folder = len([i for i in self.sub_entries if i.exists]) > 1


class FATBSubEntry(LargeContainerEntry):
    def __init__(self, f: BinaryIO, data_offset: int, i: int, vector: int) -> None:
        self.exists = (vector & 1 << i) != 0
        if self.exists:
            self.start = read_as_int(4, f, signed=True)
            self.end = read_as_int(4, f, signed=True)
            self.length = read_as_int(4, f, signed=True)
            self.parent_data_position = data_offset

    # public static string GetFileNumber(int index) => $"{index:00}";
