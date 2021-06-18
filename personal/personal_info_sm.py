from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from utils import read_as_int

from .personal_info_xy import PersonalInfoXY

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoSM(PersonalInfoXY):
    _SIZE = 0x54
    _TYPE = "garc_last_file"
    _PATH = join("a", "0", "1", "7")
    _MAX_ID = 802

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.special_tutors = [self._get_bits(0x3C, 0x0A)]

        self.special_z_item = read_as_int(2, self._data, 0x4C)
        self.special_z_basemove = read_as_int(2, self._data, 0x4E)
        self.special_z_zmove = read_as_int(2, self._data, 0x50)

        self.local_variant = bool(self._data[0x52])

        self.pokedex_numbers = {
            "original-alola": 0,
            "original-melemele": 0,
            "original-akala": 0,
            "original-ulaula": 0,
            "original-poni": 0,
        }
