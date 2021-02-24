from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from .personal_info_bw import PersonalInfoBW

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoXY(PersonalInfoBW):
    _SIZE = 0x40
    # _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    # _MAX_ID = 809

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
