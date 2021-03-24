from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from base import BaseInfo
from evolution.evolution_set import Evolution, EvolutionSet

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfo(BaseInfo):
    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.hp: int
        self.attack: int
        self.defense: int
        self.speed: int
        self.special_attack: int
        self.special_defense: int

        self.ev_hp: int
        self.ev_attack: int
        self.ev_defense: int
        self.ev_speed: int
        self.ev_special_attack: int
        self.ev_special_defense: int

        self.types: tuple[int, int]
        self.egg_groups: tuple[int, int]

        self.catch_rate: int
        self.evo_stage: int
        self.items: list[int]
        self.gender: int
        self.hatch_cycles: int
        self.base_friendship: int
        self.exp_growth: int
        self.abilities: list[int]
        self.escape_rate: int
        self.forme_count: int
        self._form_stats_index: int
        self.forme_sprite: int
        self.base_exp: int
        self._color: int

        self.height: int
        self.weight: int

        self.tmhm: dict[int, bool]
        self.type_tutors: list[bool]
        self.special_tutors: list[list[bool]]

        self.pokedex_numbers: dict[str, int]

        self.is_present_in_game: bool = True

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

    @property
    def bst(self) -> int:
        return (
            self.hp
            + self.attack
            + self.defense
            + self.speed
            + self.special_attack
            + self.special_defense
        )

    def _get_bits(self, start: int = 0, length: int = -1) -> list[bool]:
        if length < 0:
            length = len(self._data)
        result = []
        for i in range(length << 3):
            result.append(bool(self._data[start + (i >> 3)] >> (i & 0x7) & 0x1))
        return result

    def forme_index(self, species: int, forme: int) -> int:
        if forme <= 0:  # no forme requested
            return species
        if self._form_stats_index <= 0:  # no formes present
            return species
        if forme >= self.forme_count:  # beyond range of species' formes
            return species

        return self._form_stats_index + forme - 1

    ###############

    @cached_property
    def evos(self) -> list[Evolution]:
        if self._table._format not in EvolutionSet._PATHS:
            return []
        return EvolutionSet(
            self._path, self._id, self._table._format
        ).possible_evolutions

    @property
    def gender_ratio(self) -> int:
        ratios = {
            0: 0,
            31: 1,
            63: 2,
            127: 4,
            191: 6,
            225: 7,
            254: 8,
            255: -1,
        }
        return ratios[self.gender]

    @property
    def is_baby(self) -> bool:
        if self.evo_stage == 1 and 15 in self.egg_groups:  # undiscovered
            for evo in self.evos:
                evo_data = self._table.get_forme_entry(evo.species, evo.form)
                if 15 not in evo_data.egg_groups:  # undiscovered
                    return True
        return False

    def stat(self, stat_id: int) -> int:
        return {
            1: self.hp,
            2: self.attack,
            3: self.defense,
            4: self.special_attack,
            5: self.special_defense,
            6: self.speed,
        }[stat_id]

    def ev_stat(self, stat_id: int) -> int:
        return {
            1: self.ev_hp,
            2: self.ev_attack,
            3: self.ev_defense,
            4: self.ev_special_attack,
            5: self.ev_special_defense,
            6: self.ev_speed,
        }[stat_id]

    @property
    def color(self) -> int:
        return {0: 8, 1: 2, 2: 10, 3: 5, 4: 1, 5: 3, 6: 7, 7: 4, 8: 9, 9: 6}[
            self._color
        ]
