from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from utils import get_flag, read_as_int

from .personal_info_xy import PersonalInfoXY

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoSwSh(PersonalInfoXY):
    _SIZE = 0xB0
    _PATH = join("bin", "pml", "personal", "personal_total.bin")
    _MAX_ID = 898

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.abilities = [read_as_int(2, self._data, 0x18 + (i * 2)) for i in range(3)]
        self.escape_rate = 0  # moved?
        self._form_stats_index = read_as_int(2, self._data, 0x1E)
        self._color = int(self._data[0x21] & 0x3F)

        self.tmhm = dict(
            enumerate(
                [get_flag(self._data, 0x28 + (i >> 3), i) for i in range(100)]  # TMs
                + [get_flag(self._data, 0x3C + (i >> 3), i) for i in range(100)]  # TRs
            )
        )

        self.type_tutors = [get_flag(self._data, 0x38, i) for i in range(8)]

        self.special_tutors = [
            [get_flag(self._data, 0xA8 + (i >> 3), i) for i in range(18)]
        ]

        self.pokedex_numbers = {
            "galar": read_as_int(2, self._data, 0x5C),
            "isle-of-armor": read_as_int(2, self._data, 0xAC),
            "crown-tundra": read_as_int(2, self._data, 0xAE),
        }

        self.is_present_in_game = bool((self._data[0x21] >> 6) & 1)
        self.sprite_forme = bool((self._data[0x21] >> 7) & 1)
        self.sprite_index = read_as_int(2, self._data, 0x4C)
        self.regional_flags = read_as_int(2, self._data, 0x5A)
        self.is_regional_form = bool(self.regional_flags & 1)
        self.can_not_dynamax = bool((self._data[0x5A] >> 2) & 1)
