from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from utils import read_as_int

from .personal_info import PersonalInfo

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoBW(PersonalInfo):
    _SIZE = 0x3C
    _TYPE = "singlefile_noheader"
    # _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    # _MAX_ID = 809

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.hp = int(self._data[0x00])
        self.attack = int(self._data[0x01])
        self.defense = int(self._data[0x02])
        self.speed = int(self._data[0x03])
        self.special_attack = int(self._data[0x04])
        self.special_defense = int(self._data[0x05])

        self._ev_yield = read_as_int(2, self._data, 0x0A)
        self.ev_hp = self._ev_yield >> 0 & 0x3
        self.ev_attack = self._ev_yield >> 2 & 0x3
        self.ev_defense = self._ev_yield >> 4 & 0x3
        self.ev_speed = self._ev_yield >> 6 & 0x3
        self.ev_special_attack = self._ev_yield >> 8 & 0x3
        self.ev_special_defense = self._ev_yield >> 10 & 0x3

        self.types = (
            int(self._data[0x06]) + 1,
            int(self._data[0x07]) + 1,
        )
        self.egg_groups = (
            int(self._data[0x16]),
            int(self._data[0x17]),
        )

        self.catch_rate = int(self._data[0x08])
        self.evo_stage = int(self._data[0x09])
        self.items = [read_as_int(2, self._data, 0x0C + (i * 2)) for i in range(3)]
        self.gender = int(self._data[0x12])
        self.hatch_cycles = int(self._data[0x13])
        self.base_friendship = int(self._data[0x14])
        self.exp_growth = {0: 2, 1: 5, 2: 6, 3: 4, 4: 3, 5: 1}[int(self._data[0x15])]
        self.abilities = [int(self._data[0x18 + i]) for i in range(3)]
        self.escape_rate = int(self._data[0x1B])
        self.forme_count = int(self._data[0x20])
        self._form_stats_index = read_as_int(2, self._data, 0x1C)
        self.forme_sprite = read_as_int(2, self._data, 0x1E)  # ???
        self.base_exp = read_as_int(2, self._data, 0x22)
        self._color = int(self._data[0x21])
        self.height = read_as_int(2, self._data, 0x24)
        self.weight = read_as_int(2, self._data, 0x26)

        self.tmhm = self._get_bits(0x28, 0x10)
        self.type_tutors = self._get_bits(0x38, 0x04)
