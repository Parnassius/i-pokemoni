from __future__ import annotations

from os.path import join

from utils import get_flag, read_as_int

from .personal_info import PersonalInfo


class PersonalTable:
    _PATHS = {"swsh": join("bin", "pml", "personal", "personal_total.bin")}
    _LAST_SPECIES_ID = {"swsh": 898}

    def __init__(self, path: str, file_format: str) -> None:
        self._format = file_format
        with open(join(path, self._PATHS[self._format]), "rb") as f:
            self._data = f.read()
        self._size = PersonalInfo.SIZES[self._format]
        self._entries = [
            self._data[i : i + self._size]
            for i in range(0, len(self._data), self._size)
        ]
        self._table = [
            PersonalInfo(self, path, i, data, self._format)
            for i, data in enumerate(self._entries)
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
        return self._LAST_SPECIES_ID[self._format]
