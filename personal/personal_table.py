from __future__ import annotations

from collections.abc import Sequence
from os.path import join
from typing import Literal, overload

from utils import get_flag, read_as_int

from .personal_info import PersonalInfo
from .personal_info_letsgo import PersonalInfoLetsGo
from .personal_info_swsh import PersonalInfoSwSh


class PersonalTable:
    def __init__(self, path: str, file_format: str) -> None:
        self._PersonalInfo: type[PersonalInfo] = {
            "letsgo": PersonalInfoLetsGo,
            "swsh": PersonalInfoSwSh,
        }[file_format]
        self._path = path
        self._format = file_format
        with open(join(path, self._PersonalInfo._PATH), "rb") as f:
            self._data = f.read()
        self._size = self._PersonalInfo._SIZE
        self._entries = [
            self._data[i : i + self._size]
            for i in range(0, len(self._data), self._size)
        ]
        self._table = [
            self._PersonalInfo(self, self._path, pokemon_id, data)
            for pokemon_id, data in enumerate(self._entries)
        ]

    def get_personal_info(self, index: int) -> PersonalInfo:
        if 0 <= index < len(self._table):
            return self._table[index]
        return self._table[0]

    def get_forme_index(self, species: int, forme: int = 0) -> int:
        if species > self.last_species_id:
            print(species, forme)
            raise Exception("Invalid species id")
        return self.get_personal_info(species).forme_index(species, forme)

    def get_forme_entry(self, species: int, forme: int = 0) -> PersonalInfo:
        return self.get_personal_info(self.get_forme_index(species, forme))

    @property
    def last_species_id(self) -> int:
        return self._PersonalInfo._LAST_SPECIES_ID

    @overload
    @classmethod
    def get(cls, path: str, file_format: Literal["letsgo"]) -> list[PersonalInfoLetsGo]:
        ...

    @overload
    @classmethod
    def get(cls, path: str, file_format: Literal["swsh"]) -> list[PersonalInfoSwSh]:
        ...

    # suppress "Overloaded function implementation cannot produce return type ..."
    @classmethod  # type: ignore[misc]
    def get(cls, path: str, file_format: str) -> Sequence[PersonalInfo]:
        return cls(path, file_format)._table
