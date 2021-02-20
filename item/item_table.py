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

        if self._size is None:  # different file for each item
            self._table = []
            for item_id in range(self._ItemInfo._MAX_ITEM_ID + 1):
                with open(
                    join(path, self._ItemInfo._PATH.format(item_id=item_id)), "rb"
                ) as f:
                    self._table.append(self._ItemInfo(self, path, item_id, f.read()))
        else:  # single file
            with open(join(path, self._ItemInfo._PATH), "rb") as f:
                self._data = f.read()
            entries_start = read_as_int(4, self._data, 0x40)
            self._entries = [
                self._data[i : i + self._size]
                for i in range(entries_start, len(self._data), self._size)
            ]
            self._table = [
                self._ItemInfo(self, path, item_id, data)
                for item_id, data in enumerate(self._entries)
            ]

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
