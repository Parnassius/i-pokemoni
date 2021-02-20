from __future__ import annotations

from functools import cached_property
from os.path import join
from typing import TYPE_CHECKING

from evolution.evolution_set import Evolution, EvolutionSet
from utils import get_flag, read_as_int

from .personal_info_sm import PersonalInfoSM

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoLetsGo(PersonalInfoSM):
    _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    _LAST_SPECIES_ID = 809
    _FORMAT = "letsgo"

    def __init__(
        self, table: PersonalTable, path: str, pokemon_id: int, data: bytes
    ) -> None:
        super().__init__(table, path, pokemon_id, data)

        self.go_species = read_as_int(2, self._data, 0x48)

        self.pokedex_numbers = {}
        if pokemon_id <= 151:
            self.pokedex_numbers["letsgo-kanto"] = pokemon_id
        elif pokemon_id == 808:  # meltan
            self.pokedex_numbers["letsgo-kanto"] = 152
        elif pokemon_id == 809:  # melmetal
            self.pokedex_numbers["letsgo-kanto"] = 153
