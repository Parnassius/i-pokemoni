from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from .personal_info_sm import PersonalInfoSM

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoUsUm(PersonalInfoSM):
    _MAX_ID = 807

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.pokedex_numbers = {
            "updated-alola": 0,
            "updated-melemele": 0,
            "updated-akala": 0,
            "updated-ulaula": 0,
            "updated-poni": 0,
        }
