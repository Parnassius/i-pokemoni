from __future__ import annotations

from collections.abc import Sequence
from os.path import join
from typing import Literal, overload

from utils import read_as_int

from .item_info import ItemInfo
from .item_info_letsgo import ItemInfoLetsGo
from .item_info_swsh import ItemInfoSwSh


class ItemTable:
    def __init__(self, path: str, file_format: str) -> None:
        self._ItemInfo: type[ItemInfo] = {
            "letsgo": ItemInfoLetsGo,
            "swsh": ItemInfoSwSh,
        }[file_format]
        self._path = path
        self._format = file_format
        self._size = self._ItemInfo._SIZE

        self._table = []
        if self._size is None:  # different file for each item
            for item_id in range(self._ItemInfo._MAX_ITEM_ID + 1):
                with open(
                    join(path, self._ItemInfo._PATH.format(item_id=item_id)), "rb"
                ) as f:
                    self._table.append(self._ItemInfo(self, path, item_id, f.read()))
        else:  # single file
            with open(join(path, self._ItemInfo._PATH), "rb") as f:
                self._data = f.read()
            num_entries = read_as_int(2, self._data, 0x0)
            max_entry_index = read_as_int(2, self._data, 0x4)
            entries_start = read_as_int(4, self._data, 0x40, True)
            for item_id in range(num_entries):
                entry_index = read_as_int(2, self._data, 0x44 + (2 * item_id))
                if entry_index >= max_entry_index:
                    raise Exception
                start = entries_start + (entry_index * self._size)
                end = start + self._size
                self._table.append(
                    self._ItemInfo(self, path, item_id, self._data[start:end])
                )

    def get_item_info(self, index: int) -> ItemInfo:
        return self._table[index]

    @overload
    @classmethod
    def get(cls, path: str, file_format: Literal["letsgo"]) -> list[ItemInfoLetsGo]:
        ...

    @overload
    @classmethod
    def get(cls, path: str, file_format: Literal["swsh"]) -> list[ItemInfoSwSh]:
        ...

    # suppress "Overloaded function implementation cannot produce return type ..."
    @classmethod  # type: ignore[misc]
    def get(cls, path: str, file_format: str) -> Sequence[ItemInfo]:
        return cls(path, file_format)._table
