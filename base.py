from __future__ import annotations

from collections.abc import Callable, Mapping
from os.path import join
from typing import Generic, Type, TypeVar, cast

import lz4.block  # type: ignore

from utils import read_as_int


class BaseInfo:
    _SKIP: bool = False
    _CUSTOM_FUNCTION: Callable[[type[T], BaseTable], list[T]] | None = None
    _TYPE: str
    _SIZE: int = 0
    _MAX_ID: int = 0
    _SEARCH_PATTERN: bytes = b""
    _SEARCH_OFFSET: int = 0
    _PATH: str

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        self._table = table
        self._path = path
        self._id = id
        self._data = data


T = TypeVar("T", bound=BaseInfo)


class BaseTable(Generic[T]):
    _CLASSES: Mapping[str, type[BaseInfo]]

    def __init__(self, path: str, file_format: str) -> None:
        self._cls = cast(Type[T], self._CLASSES[file_format])
        self._path = path
        self._format = file_format

        self._table: list[T] = self._open_data_files()

    def get_info_from_index(self, index: int) -> T:
        return self._table[index]

    @property
    def max_id(self) -> int:
        return self._cls._MAX_ID

    def _open_data_files(self) -> list[T]:
        if self._cls._SKIP:
            return []
        if self._cls._CUSTOM_FUNCTION:
            return self._cls._CUSTOM_FUNCTION(self._cls, self)
        return {
            "multiplefiles": self._open_multiple_files,
            "singlefile": self._open_single_file,
            "singlefile_noheader": self._open_single_file_no_header,
            "mini": self._open_mini,
            "gfpak": self._open_gfpak,
            "nso_text": self._open_nso,
            "nso_ro": self._open_nso,
            "nso_data": self._open_nso,
        }[self._cls._TYPE]()

    def _open_multiple_files(self) -> list[T]:
        table = []

        for id in range(self._cls._MAX_ID + 1):
            with open(join(self._path, self._cls._PATH.format(id=id)), "rb") as f:
                table.append(self._cls(self, self._path, id, f.read()))

        return table

    def _open_single_file(self) -> list[T]:
        table = []

        with open(join(self._path, self._cls._PATH), "rb") as f:
            self._data = f.read()

        num_entries = read_as_int(2, self._data, 0x0)
        max_entry_index = read_as_int(2, self._data, 0x4)
        entries_start = read_as_int(4, self._data, 0x40, True)

        for id in range(num_entries):
            entry_index = read_as_int(2, self._data, 0x44 + (2 * id))
            if entry_index >= max_entry_index:
                raise Exception
            start = entries_start + (entry_index * self._cls._SIZE)
            end = start + self._cls._SIZE
            table.append(self._cls(self, self._path, id, self._data[start:end]))

        return table

    def _open_single_file_no_header(self) -> list[T]:
        table = []

        with open(join(self._path, self._cls._PATH), "rb") as f:
            self._data = f.read()

        entries = [
            self._data[i : i + self._cls._SIZE]
            for i in range(0, len(self._data), self._cls._SIZE)
        ]

        for id, data in enumerate(entries):
            table.append(self._cls(self, self._path, id, data))

        return table

    def _open_mini(self) -> list[T]:
        table = []

        with open(join(self._path, self._cls._PATH), "rb") as f:
            self._data = f.read()

        if len(self._data) < 4:
            raise Exception

        pos = 0x2
        count = read_as_int(2, self._data, pos)
        pos += 0x2
        start = read_as_int(4, self._data, pos, True)
        pos += 0x4

        entries = []
        for i in range(count):
            end = read_as_int(4, self._data, pos)
            pos += 4
            entries.append(self._data[start:end])
            start = end

        for id, data in enumerate(entries):
            table.append(self._cls(self, self._path, id, data))

        return table

    def _open_gfpak(self) -> list[T]:
        table = []

        with open(join(self._path, self._cls._PATH), "rb") as f:
            self._data = f.read()

        num_files = read_as_int(4, self._data, 0x10, True)
        num_folders = read_as_int(4, self._data, 0x14, True)

        pos = 0x28 + num_folders * 0x08 + num_files * 0x08

        for i in range(num_folders):
            num_files_in_folder = read_as_int(4, self._data, pos + 0x8, True)
            pos += 0x10 + num_files_in_folder * 0x10

        entries = []

        for i in range(num_files):
            compression_type = read_as_int(2, self._data, pos + (i * 0x18) + 0x02)
            size_decompressed = read_as_int(
                4, self._data, pos + (i * 0x18) + 0x04, True
            )

            start = read_as_int(4, self._data, pos + (i * 0x18) + 0x10, True)
            end = start + read_as_int(4, self._data, pos + (i * 0x18) + 0x08, True)

            entry = self._data[start:end]

            if compression_type == 1:  # Zlib
                raise  # not implemented
            elif compression_type == 2:  # Lz4
                entry = lz4.block.decompress(entry, size_decompressed)

            entries.append(entry)

        for id, data in enumerate(entries):
            table.append(self._cls(self, self._path, id, data))

        return table

    def _open_nso(self) -> list[T]:
        table = []

        with open(join(self._path, self._cls._PATH), "rb") as f:
            self._data = f.read()

        if len(self._data) < 0x100:
            raise Exception

        part = {"text": 0, "ro": 1, "data": 2}[self._cls._TYPE[4:]]

        flags = read_as_int(4, self._data, 0x0C)

        start = read_as_int(4, self._data, 0x10 + (0x10 * part), True)
        end = start + read_as_int(4, self._data, 0x60 + (0x04 * part), True)

        decompressed_size = read_as_int(4, self._data, 0x18 + (0x10 * part), True)

        self._data = self._data[start:end]

        if flags >> part & 1:
            self._data = lz4.block.decompress(self._data, decompressed_size)

        offset = self._data[self._cls._SEARCH_OFFSET :].find(self._cls._SEARCH_PATTERN)
        if offset < len(self._cls._SEARCH_PATTERN):
            print("oh no")
            o_ = self._data.find(bytes([25, 0, 6, 0, 7, 0, 8, 0, 9, 0, 19, 0, 42, 0]))
            print(o_)
            exit()
        offset += self._cls._SEARCH_OFFSET + len(self._cls._SEARCH_PATTERN)

        self._data = self._data[offset:]

        entries = [
            self._data[i : i + self._cls._SIZE]
            for i in range(
                0, self._cls._SIZE * (self._cls._MAX_ID + 1), self._cls._SIZE
            )
        ]

        for id, data in enumerate(entries):
            table.append(self._cls(self, self._path, id, data))

        return table
