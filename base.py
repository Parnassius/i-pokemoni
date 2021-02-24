from __future__ import annotations

from collections.abc import Mapping
from os.path import join
from typing import Generic, Type, TypeVar, cast

from utils import read_as_int, read_mini


class BaseInfo:
    _TYPE: str
    _SIZE: int = 0
    _MAX_ID: int = 0
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
        self._size = self._cls._SIZE
        self._type = self._cls._TYPE

        self._table: list[T] = self._open_data_files()

    def _open_data_files(self) -> list[T]:
        table = []

        if self._type == "multiplefiles":
            for id in range(self._cls._MAX_ID + 1):
                with open(join(self._path, self._cls._PATH.format(id=id)), "rb") as f:
                    table.append(self._cls(self, self._path, id, f.read()))

        elif self._type == "singlefile":
            with open(join(self._path, self._cls._PATH), "rb") as f:
                self._data = f.read()
            num_entries = read_as_int(2, self._data, 0x0)
            max_entry_index = read_as_int(2, self._data, 0x4)
            entries_start = read_as_int(4, self._data, 0x40, True)
            for id in range(num_entries):
                entry_index = read_as_int(2, self._data, 0x44 + (2 * id))
                if entry_index >= max_entry_index:
                    raise Exception
                start = entries_start + (entry_index * self._size)
                end = start + self._size
                table.append(self._cls(self, self._path, id, self._data[start:end]))

        elif self._type == "singlefile_noheader":
            with open(join(self._path, self._cls._PATH), "rb") as f:
                self._data = f.read()
            entries = [
                self._data[i : i + self._size]
                for i in range(0, len(self._data), self._size)
            ]
            table = [
                self._cls(self, self._path, pokemon_id, data)
                for pokemon_id, data in enumerate(entries)
            ]

        elif self._type == "mini":
            with open(join(self._path, self._cls._PATH), "rb") as f:
                self._data = f.read()
            for id, data in enumerate(read_mini(self._data)):
                table.append(self._cls(self, self._path, id, data))

        return table

    def get_info_from_index(self, index: int) -> T:
        return self._table[index]

    @property
    def max_id(self) -> int:
        return self._cls._MAX_ID
