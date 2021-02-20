from __future__ import annotations

from functools import cached_property
from os.path import join
from typing import TYPE_CHECKING

from evolution.evolution_set import Evolution, EvolutionSet
from utils import get_flag, read_as_int

from .personal_info_bw import PersonalInfoBW

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoXY(PersonalInfoBW):
    _SIZE = 0x40
    # _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    # _LAST_SPECIES_ID = 809
    _FORMAT = "xy"

    def __init__(
        self, table: PersonalTable, path: str, pokemon_id: int, data: bytes
    ) -> None:
        super().__init__(table, path, pokemon_id, data)
