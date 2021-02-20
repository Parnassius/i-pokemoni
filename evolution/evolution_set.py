from __future__ import annotations

from os.path import join

from utils import read_as_int


class Evolution:
    def __init__(
        self, method: int, argument: int, species: int, form: int, level: int
    ) -> None:
        self._method = method
        self.argument = argument
        self.species = species
        self.form = form
        self.level = level

    @property
    def method(self) -> int:
        """
        1 => golbat (level + friendship)
        2 => budew (level + friendship + day)
        3 => snom (level + friendship + night)
        4 => bulbasaur (level)
        5 => kadabra (trade)
        6 => poliwhirl (trade + item)
        7 => karrablast (trade with pokemon)  # hardcoded?
        8 => pikachu (item)
        9 => tyrogue (level + atk>def)
        10 => tyrogue (level + atk=def)
        11 => tyrogue (level + atk<def)
        14 => nincada (shed)
        16 => feebas (beauty)  # argument = min beauty
        17 => kirlia (dawn stone + male)  # argument = 109, dawn stone?
        18 => snorunt (dawn stone + female)  # argument = 109, dawn stone?
        19 => happiny (level + item + day)
        20 => sneasel (level + item)
        21 => lickitung (level + move)
        22 => mantyke (level + pokemon in party)  # argument is the needed pokemon
        23 => espurr (level + male)
        24 => combee (level + female)
        28 => inkay (level + upside down)
        29 => sylveon (level + fairy move + affection/friendship)  # argument = 17, maybe fairy?
        30 => pancham (level + dark type pokemon in party)  # argument is 0, so dark should be hardcoded
        31 => sliggoo (level + rain or fog)
        32 => tyrunt (level + day)
        33 => amaura (level + night)
        34 => espurr (level + female)
        36 => cosmoem (level + game)  # solgaleo in sun/ultrasun/sword (argument 44), lunala in moon/ultramoon/shield (argument 45)
        45 => milcery (spin)  # hardcoded?
        46 => toxel (level + amped nature)
        47 => toxel (level + low key nature)
        48 => kubfu (single strike tower)
        49 => kubfu (rapid strike tower)

        items
        221 => kings rock
        233 => metal coat
        235 => dragon scale
        252 => up-grade
        321 => protector
        322 => electrizer
        323 => magmarizer
        324 => dubious disk
        325 => reaper cloth
        537 => prism scale
        646 => whipped dream
        647 => sachet
        """
        return {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 11,
            14: 14,
            16: 16,
            17: 17,
            18: 18,
            19: 19,
            20: 20,
            21: 21,
            22: 22,
            23: 23,
            24: 24,
            28: 28,
            29: 29,
            30: 30,
            31: 31,
            32: 32,
            33: 33,
            34: 34,
            36: 36,
            45: 45,
            46: 46,
            47: 47,
            48: 48,
            49: 49,
        }.get(self._method, 1000 + self._method)


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
