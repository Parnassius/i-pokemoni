from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemInfoSwSh(ItemInfo):
    _SIZE = 0x30
    _PATH = join("bin", "pml", "item", "item.dat")

    def __init__(self, table, path: str, item_id: int, data: bytes) -> None:
        super().__init__(table, path, item_id, data)
