from __future__ import annotations

from os.path import join
from typing import Literal

from utils import read_as_int


class Evolution:
    def __init__(
        self, method: int, argument: int, species: int, form: int, level: int
    ) -> None:
        self._method = method
        self._argument = argument
        self.species = species
        self.form = form
        self._level = level

        """
        self._method
        1 => level + friendship
        2 => level + friendship + day
        3 => level + friendship + night
        4 => level
        5 => trade
        6 => trade + held item
        7 => trade with pokemon  # hardcoded, shelmet/karrablast
        8 => use item
        9 => level + atk>def
        10 => level + atk=def
        11 => level + atk<def
        12 => level + personality  # wurmple => silcoon
        13 => level + personality  # wurmple => cascoon
        14 => shed
        16 => beauty
        17 => use item + male
        18 => use item + female
        19 => level + held item + day
        20 => level + held item + night
        21 => level + learnt move
        22 => level + pokemon in party
        23 => level + male
        24 => level + female
        25 => level + magnetic field
        28 => level + upside down
        29 => level + learnt type of move + friendship
        30 => level + dark type pokemon in party
        31 => level + rain
        32 => level + day
        33 => level + night
        34 => level + female
        36 => level + game  # solgaleo in sun/ultrasun/sword (argument 44), lunala in moon/ultramoon/shield (argument 45)
        37 => level + day + game  # sun/ultrasun
        38 => level + night + game  # moon/ultramoon
        39 => level + mount lanakila
        45 => spin  # form should be hardcoded
        46 => level + amped nature
        47 => level + low key nature
        48 => single strike tower
        49 => rapid strike tower
        """

    @property
    def skip_record(self) -> bool:
        return self._method in (25, 39)

    @property
    def trigger_id(self) -> int:
        if self._method in (
            1,
            2,
            3,
            4,
            9,
            10,
            11,
            12,
            13,
            16,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            36,
            37,
            38,
            39,
            46,
            47,
        ):
            return 1  # level-up
        if self._method in (5, 6, 7):
            return 2  # trade
        if self._method in (8, 17, 18):
            return 3  # use-item
        if self._method == 14:
            return 4  # shed
        if self._method == 45:
            return 5  # spin
        if self._method == 48:
            return 6  # tower-of-darkness
        if self._method == 49:
            return 7  # tower-of-waters
        raise Exception("missing evolution_trigger_id: " + str(self._method))

    @property
    def trigger_item_id(self) -> int:
        if self.trigger_id == 3:  # use-item
            return self._argument
        return 0

    @property
    def level(self) -> int:
        if self.trigger_id == 1:  # level-up
            return self._level
        return 0

    @property
    def gender_id(self) -> int:
        if self._method in (17, 23):
            return 1  # male
        if self._method in (18, 24, 34):
            return 2  # female
        return 0

    @property
    def held_item_id(self) -> int:
        if self._method in (6, 19, 20):
            return self._argument
        return 0

    @property
    def time_of_day(self) -> str:
        if self._method in (2, 19, 32, 37):
            return "day"
        if self._method in (3, 20, 33, 38):
            return "night"
        return ""

    @property
    def known_move_id(self) -> int:
        if self._method == 21:
            return self._argument
        return 0

    @property
    def known_move_type_id(self) -> int:
        if self._method == 29:
            return self._argument + 1
        return 0

    @property
    def minimum_happiness(self) -> int:
        if self._method in (1, 2, 3, 29):
            return 160
        return 0

    @property
    def minimum_beauty(self) -> int:
        if self._method == 16:
            return self._argument
        return 0

    @property
    def relative_physical_stats(self) -> int | Literal[""]:
        if self._method == 9:
            return 1
        if self._method == 10:
            return 0
        if self._method == 11:
            return -1
        return ""

    @property
    def party_species_id(self) -> int:
        if self._method == 22:
            return self._argument
        return 0

    @property
    def party_type_id(self) -> int:
        if self._method == 30:
            return 17  # dark
        return 0

    @property
    def trade_species_id(self) -> int:
        if self._method == 7:
            return {
                589: 616,  # escavalier: shelmet
                617: 588,  # accelgor: karrablast
            }[self.species]
        return 0

    @property
    def needs_overworld_rain(self) -> bool:
        return self._method == 31

    @property
    def turn_upside_down(self) -> bool:
        return self._method == 28


class EvolutionSet:
    _PATHS = {
        "letsgo": ["bin", "pokelib", "evolution", "evo_{id:0>3}.bin"],
        "swsh": ["bin", "pml", "evolution", "evo_{id:0>3}.bin"],
    }

    _ENTRY_SIZES = {"letsgo": 8, "swsh": 8}
    _ENTRY_COUNTS = {"letsgo": 8, "swsh": 9}
    SIZES = {
        i[0]: i[1] * i[2]
        for i in zip(_ENTRY_SIZES.keys(), _ENTRY_SIZES.values(), _ENTRY_COUNTS.values())
    }

    def __init__(self, path: str, pokemon_id: int, file_format: str) -> None:
        self._format = file_format

        path = join(path, *[i.format(id=pokemon_id) for i in self._PATHS[self._format]])
        with open(path, "rb") as f:
            self._data = f.read()

    @property
    def possible_evolutions(self) -> list[Evolution]:
        result: list[Evolution] = []
        offset = self._ENTRY_SIZES[self._format]
        for i in range(self._ENTRY_COUNTS[self._format]):
            evo = Evolution(
                read_as_int(2, self._data, i * offset + 0),  # method
                read_as_int(2, self._data, i * offset + 2),  # argument
                read_as_int(2, self._data, i * offset + 4),  # species
                int(self._data[i * offset + 6]),  # form
                int(self._data[i * offset + 7]),  # level
            )
            if evo.species:
                result.append(evo)
        return result
