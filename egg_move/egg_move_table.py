from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .egg_move_info import EggMoveInfo
from .egg_move_info_letsgo import EggMoveInfoLetsGo
from .egg_move_info_sm import EggMoveInfoSM
from .egg_move_info_swsh import EggMoveInfoSwSh
from .egg_move_info_usum import EggMoveInfoUsUm


class EggMoveTable(BaseTable[EggMoveInfo]):
    _CLASSES: Mapping[str, type[EggMoveInfo]] = {
        "sm": EggMoveInfoSM,
        "usum": EggMoveInfoUsUm,
        "letsgo": EggMoveInfoLetsGo,
        "swsh": EggMoveInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
