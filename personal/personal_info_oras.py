from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from .personal_info_xy import PersonalInfoXY

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoOrAs(PersonalInfoXY):
    _SIZE = 0x50
    _TYPE = "garc_last_file"
    _PATH = join("a", "1", "9", "5")
    _MAX_ID = 721

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.special_tutors = [
            self._get_bits(0x40, 0x04)[:0x0E],
            self._get_bits(0x44, 0x04)[:0x11],
            self._get_bits(0x48, 0x04)[:0x10],
            self._get_bits(0x4C, 0x04)[:0x0E],
        ]
