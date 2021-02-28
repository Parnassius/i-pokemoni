from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from utils import read_as_int

from .personal_info_sm import PersonalInfoSM

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoLetsGo(PersonalInfoSM):
    _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    _MAX_ID = 809

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.go_species = read_as_int(2, self._data, 0x48)

        self.special_tutors = [
            [self._id == 966] * 3  # pikachu-starter
            + [self._id == 979] * 8  # eevee-starter
        ]

        self.pokedex_numbers = {}
        if self._id <= 151:
            self.pokedex_numbers["letsgo-kanto"] = self._id
        elif self._id == 808:  # meltan
            self.pokedex_numbers["letsgo-kanto"] = 152
        elif self._id == 809:  # melmetal
            self.pokedex_numbers["letsgo-kanto"] = 153
