from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .move_info import MoveInfo
from .move_info_letsgo import MoveInfoLetsGo
from .move_info_swsh import MoveInfoSwSh


class MoveTable(BaseTable[MoveInfo]):
    _CLASSES: Mapping[str, type[MoveInfo]] = {
        "letsgo": MoveInfoLetsGo,
        "swsh": MoveInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
