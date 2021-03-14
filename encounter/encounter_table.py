from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .encounter_info import EncounterInfo
from .encounter_info_letsgo import EncounterInfoLetsGo
from .encounter_info_swsh import EncounterInfoSwSh


class EncounterTable(BaseTable[EncounterInfo]):
    _CLASSES: Mapping[str, type[EncounterInfo]] = {
        "letsgo": EncounterInfoLetsGo,
        "swsh": EncounterInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
