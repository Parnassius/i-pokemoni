from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .learnset_info import LearnsetInfo
from .learnset_info_letsgo import LearnsetInfoLetsGo
from .learnset_info_oras import LearnsetInfoOrAs
from .learnset_info_sm import LearnsetInfoSM
from .learnset_info_swsh import LearnsetInfoSwSh
from .learnset_info_usum import LearnsetInfoUsUm


class LearnsetTable(BaseTable[LearnsetInfo]):
    _CLASSES: Mapping[str, type[LearnsetInfo]] = {
        "oras": LearnsetInfoOrAs,
        "sm": LearnsetInfoSM,
        "usum": LearnsetInfoUsUm,
        "letsgo": LearnsetInfoLetsGo,
        "swsh": LearnsetInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
