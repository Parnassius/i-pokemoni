from __future__ import annotations

from utils import read_as_int


class ItemInfo:
    SIZES = {"swsh": 0x30}

    def __init__(
        self, table, path: str, item_id: int, data: bytes, file_format: str
    ) -> None:
        self._table = table
        self._path = path
        self._id = item_id
        self._data = data
        self._format = file_format

    @property
    def pouch_id(self) -> int:
        return int(self._data[0x11] & 0x0F)

    @property
    def pouch(self) -> int:
        return {
            0: 2,
            1: 3,
            2: 7,
            3: 5,
            4: 1,  # items => misc?
            5: 4,
            6: 0,  # treasures
            7: 0,  # ingredients
            8: 8,
        }[self.pouch_id]

    @property
    def item_sprite(self) -> int:
        return read_as_int(2, self._data, 0x1A)

    @property
    def group_type(self) -> int:
        return int(self._data[0x1C])

    @property
    def group_index(self) -> int:
        return int(self._data[0x1D])
