from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemTable:
    _PATHS = {"swsh": join("bin", "pml", "item", "item.dat")}

    def __init__(self, path: str, file_format: str) -> None:
        self._format = file_format
        with open(join(path, self._PATHS[self._format]), "rb") as f:
            self._data = f.read()
        self._size = ItemInfo.SIZES[self._format]
        self._num_entries = read_as_int(2, self._data, 0x0)
        self._entries_start = read_as_int(4, self._data, 0x40)
        self._entries = [
            self._data[i : i + self._size]
            for i in range(self._entries_start, len(self._data), self._size)
        ]
        self._table = [
            ItemInfo(self, path, i, data, self._format)
            for i, data in enumerate(self._entries)
        ]

    def get_item_info(self, index: int) -> ItemInfo:
        return self._table[index]
