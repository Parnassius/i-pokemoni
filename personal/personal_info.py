from __future__ import annotations

from utils import get_flag, read_as_int


class PersonalInfo:
    SIZES = {
        #GameVersion.BW => PersonalInfoBW.SIZE,
        #GameVersion.B2W2 => PersonalInfoB2W2.SIZE,
        #GameVersion.XY => PersonalInfoXY.SIZE,
        #GameVersion.ORAS => PersonalInfoORAS.SIZE,
        #GameVersion.SM or GameVersion.USUM or GameVersion.GG => PersonalInfoSM.SIZE,
        "swsh": 0xB0
    }

    def __init__(self, data: bytes, format: str) -> None:
        self._data = data
        self._format = format

        self.tmhm = [False] * 200
        for i in range(len(self.tmhm) // 2):
            self.tmhm[i] = get_flag(self._data, 0x28 + (i >> 3), i)
            self.tmhm[i + 100] = get_flag(self._data, 0x3C + (i >> 3), i)

        self.type_tutors = [False] * 8
        for i in range(len(self.type_tutors)):
            self.type_tutors[i] = get_flag(self._data, 0x38, i)

        self.armor_tutors = [False] * 18
        for i in range(len(self.armor_tutors)):
            self.armor_tutors[i] = get_flag(self._data, 0xA8 + (i >> 3), i)

    @property
    def hp(self) -> int:
        return int(self._data[0x00])

    @property
    def attack(self) -> int:
        return int(self._data[0x01])

    @property
    def defense(self) -> int:
        return int(self._data[0x02])

    @property
    def speed(self) -> int:
        return int(self._data[0x03])

    @property
    def special_attack(self) -> int:
        return int(self._data[0x04])

    @property
    def special_defense(self) -> int:
        return int(self._data[0x05])

    @property
    def type_1(self) -> int:
        return int(self._data[0x06])

    @property
    def type_2(self) -> int:
        return int(self._data[0x07])

    @property
    def catch_rate(self) -> int:
        return int(self._data[0x08])

    @property
    def evo_stage(self) -> int:
        return int(self._data[0x09])

    @property
    def _ev_yield(self) -> int:
        return read_as_int(2, self._data, 0x0A)

    @property
    def ev_hp(self) -> int:
        return self._ev_yield >> 0 & 0x3

    @property
    def ev_attack(self) -> int:
        return self._ev_yield >> 2 & 0x3

    @property
    def ev_defense(self) -> int:
        return self._ev_yield >> 4 & 0x3

    @property
    def ev_speed(self) -> int:
        return self._ev_yield >> 6 & 0x3

    @property
    def ev_special_attack(self) -> int:
        return self._ev_yield >> 8 & 0x3

    @property
    def ev_special_defense(self) -> int:
        return self._ev_yield >> 10 & 0x3

    @property
    def item_1(self) -> int:
        return read_as_int(2, self._data, 0x0C)

    @property
    def item_2(self) -> int:
        return read_as_int(2, self._data, 0x0E)

    @property
    def item_3(self) -> int:
        return read_as_int(2, self._data, 0x10)

    @property
    def gender(self) -> int:
        return int(self._data[0x12])

    @property
    def hatch_cycles(self) -> int:
        return int(self._data[0x13])

    @property
    def base_friendship(self) -> int:
        return int(self._data[0x14])

    @property
    def exp_growth(self) -> int:
        return int(self._data[0x15])

    @property
    def egg_group_1(self) -> int:
        return int(self._data[0x16])

    @property
    def egg_group_2(self) -> int:
        return int(self._data[0x17])

    @property
    def ability_1(self) -> int:
        return read_as_int(2, self._data, 0x18)

    @property
    def ability_2(self) -> int:
        return read_as_int(2, self._data, 0x1A)

    @property
    def ability_h(self) -> int:
        return read_as_int(2, self._data, 0x1C)

    @property
    def escape_rate(self) -> int:
        return 0  # moved?

    @property
    def _form_stats_index(self) -> int:
        return read_as_int(2, self._data, 0x1E)

    @property
    def forme_sprite(self) -> int:
        return read_as_int(2, self._data, 0x1E)  # ???

    @property
    def forme_count(self) -> int:
        return int(self._data[0x20])

    @property
    def color(self) -> int:
        return int(self._data[0x21] & 0x3F)

    @property
    def is_present_in_game(self) -> bool:
        return bool((self._data[0x21] >> 6) & 1)

    @property
    def sprite_forme(self) -> bool:
        return bool((self._data[0x21] >> 7) & 1)

    @property
    def base_exp(self) -> int:
        return read_as_int(2, self._data, 0x22)

    @property
    def height(self) -> int:
        return read_as_int(2, self._data, 0x23)

    @property
    def weight(self) -> int:
        return read_as_int(2, self._data, 0x24)

    @property
    def sprite_index(self) -> int:
        return read_as_int(2, self._data, 0x4C)

    @property
    def regional_flags(self) -> int:
        return read_as_int(2, self._data, 0x5A)

    @property
    def is_regional_form(self) -> bool:
        return bool(self.regional_flags & 1)

    @property
    def can_not_dynamax(self) -> bool:
        return bool((self._data[0x5A] >> 2) & 1)

    @property
    def pokedex_index(self) -> int:
        return read_as_int(2, self._data, 0x5C)

    @property
    def armordex_index(self) -> int:
        return read_as_int(2, self._data, 0xAC)

    @property
    def crowndex_index(self) -> int:
        return read_as_int(2, self._data, 0xAE)

    ####################

    def forme_index(self, species: int, forme: int) -> int:
        if forme <= 0:  # no forme requested
            return species
        if self._form_stats_index <= 0:  # // no formes present
            return species
        if forme >= self.forme_count:  # beyond range of species' formes
            return species

        return self._form_stats_index + forme - 1

    @property
    def is_dual_gender(self) -> bool:
        return self.fixed_gender < 0

    @property
    def fixed_gender(self) -> int:
        if self.genderless:
            return 2
        if self.only_female:
            return 1
        if self.only_male:
            return 0
        return -1

    @property
    def genderless(self) -> bool:
        return self.gender == 255

    @property
    def only_female(self) -> bool:
        return self.gender == 254

    @property
    def only_male(self) -> bool:
        return self.gender == 0

    @property
    def has_formes(self) -> bool:
        return self.forme_count > 1
