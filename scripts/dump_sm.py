from __future__ import annotations

from os.path import join

from paths import PATHS
from utils import read_as_int

from .dump_base import DumpBase


class DumpSM(DumpBase):
    _SECTIONS = ["learnsets"]

    _region_id = 7
    _region_identifier = "alola"
    _region_names = {9: "Alola"}

    _generation_id = 7
    _generation_identifier = "generation-vii"
    _generation_main_region = 7
    _generation_names = {9: "Generation VII"}

    _version_group_id = 17
    _version_group_identifier = "sun-moon"
    _version_group_order = 17

    _version_ids = [27, 28]
    _version_identifiers = ["sun", "moon"]
    _version_names = [
        {9: "Sun"},
        {9: "Moon"},
    ]

    _pokedex_ids = [16, 17, 18, 19, 20]
    _pokedex_identifiers = [
        "original-alola",
        "original-melemele",
        "original-akala",
        "original-ulaula",
        "original-poni",
    ]
    _pokedex_names = [
        {9: ("Original Alola", "")},
        {9: ("Original Melemele", "")},
        {9: ("Original Akala", "")},
        {9: ("Original Ula'ula", "")},
        {9: ("Original Poni", "")},
    ]

    _type_tutors = [
        520,  # grass-pledge
        519,  # fire-pledge
        518,  # water-pledge
        338,  # frenzy-plant
        307,  # blast-burn
        308,  # hydro-cannon
        434,  # draco-meteor
        620,  # dragon-ascent
    ]
    _hardcode_tutors = {
        648: 547,  # meloetta / relic-song
        10018: 547,  # meloetta-pirouette / relic-song
        647: 548,  # keldeo / secret-sword
        10024: 548,  # keldeo-resolute / secret-sword
        25: 344,  # pikachu / volt-tackle
    }

    def __init__(self, sections: list) -> None:
        self._path = PATHS["sun"]
        self._format = "sm"

        super().__init__(sections)
