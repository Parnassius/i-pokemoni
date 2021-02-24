from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .item_info import ItemInfo
from .item_info_letsgo import ItemInfoLetsGo
from .item_info_swsh import ItemInfoSwSh


class ItemTable(BaseTable[ItemInfo]):
    _CLASSES: Mapping[str, type[ItemInfo]] = {
        "letsgo": ItemInfoLetsGo,
        "swsh": ItemInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
