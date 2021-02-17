from __future__ import annotations

from os.path import join
from typing import NamedTuple

from utils import read_as_int


class Evolution(NamedTuple):
    method: int
    argument: int
    species: int
    form: int
    level: int


class EvolutionSet:
    _PATHS = {"swsh": ["bin", "pml", "evolution", "evo_{id:0>3}.bin"]}

    _ENTRY_SIZES = {"swsh": 8}
    _ENTRY_COUNTS = {"swsh": 9}
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
