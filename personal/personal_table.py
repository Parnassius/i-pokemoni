from __future__ import annotations

from utils import get_flag, read_as_int

from personal_info import PersonalInfo


class PersonalTable:
    def __init__(self, filename: str, format: str) -> None:
        self._filename = filename
        with open(filename, "rb") as f:
            self._data = f.read()
        self._size = PersonalInfo.SIZES[format]
        self._entries = [self._data[i:i+self._size] for i in range(0, len(self._data), self._size)]
        self._table = [PersonalInfo(i, format) for i in self._entries]


    def get_personal_info(self, index: int) -> PersonalInfo:
        if 0 <= index < len(self._table):
            return self._table[index]
        return self._table[0]

    def get_forme_index(self, species: int, forme: int) -> int:
        return self.get_personal_info(species).forme_index(species, forme)

    def get_forme_entry(self, species: int, forme: int) -> PersonalInfo:
        return self.get_personal_info(self.get_forme_index(species, forme))


t = PersonalTable("/home/luca/Documents/repos/pokemon_data/swsh393216/Pokémon Sword [v393216]/RomFS/bin/pml/personal/personal_total.bin", "swsh")

breakpoint()
