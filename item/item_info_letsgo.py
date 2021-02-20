from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemInfoLetsGo(ItemInfo):
    _SIZE = None
    _MAX_ITEM_ID = 1057
    _PATH = join("bin", "pokelib", "item", "item{item_id:0>3}.dat")

    def __init__(self, table, path: str, item_id: int, data: bytes) -> None:
        super().__init__(table, path, item_id, data)
