from __future__ import annotations

from functools import cached_property
from os.path import join
from typing import TYPE_CHECKING

from evolution.evolution_set import Evolution, EvolutionSet
from utils import get_flag, read_as_int

from .personal_info_xy import PersonalInfoXY

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoSM(PersonalInfoXY):
    _SIZE = 0x54
    # _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    # _LAST_SPECIES_ID = 809
    _FORMAT = "sm"

    def __init__(
        self, table: PersonalTable, path: str, pokemon_id: int, data: bytes
    ) -> None:
        super().__init__(table, path, pokemon_id, data)

        self.special_tutors = self._get_bits(0x3C, 0x0A)

        self.special_z_item = read_as_int(2, self._data, 0x4C)
        self.special_z_basemove = read_as_int(2, self._data, 0x4E)
        self.special_z_zmove = read_as_int(2, self._data, 0x50)

        self.local_variant = bool(self._data[0x52])