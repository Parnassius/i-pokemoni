from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .personal_info import PersonalInfo
from .personal_info_letsgo import PersonalInfoLetsGo
from .personal_info_sm import PersonalInfoSM
from .personal_info_swsh import PersonalInfoSwSh
from .personal_info_usum import PersonalInfoUsUm


class PersonalTable(BaseTable[PersonalInfo]):
    _CLASSES: Mapping[str, type[PersonalInfo]] = {
        "sm": PersonalInfoSM,
        "usum": PersonalInfoUsUm,
        "letsgo": PersonalInfoLetsGo,
        "swsh": PersonalInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)

    def get_forme_index(self, species: int, forme: int = 0) -> int:
        if species > self.max_id:
            print(species, forme)
            raise Exception("Invalid species id")
        return self.get_info_from_index(species).forme_index(species, forme)

    def get_forme_entry(self, species: int, forme: int = 0) -> PersonalInfo:
        return self.get_info_from_index(self.get_forme_index(species, forme))
