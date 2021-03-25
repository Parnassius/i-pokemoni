from __future__ import annotations

from os.path import join

from paths import PATHS
from utils import read_as_int

from .dump_base import DumpBase


class DumpOrAs(DumpBase):
    _SECTIONS = ["learnsets"]

    _region_id = 3
    _region_identifier = "hoenn"
    _region_names = {9: "Hoenn"}

    _generation_id = 6
    _generation_identifier = "generation-vi"
    _generation_main_region = 6
    _generation_names = {9: "Generation VI"}

    _version_group_id = 16
    _version_group_identifier = "omega-ruby-alpha-sapphire"
    _version_group_order = 16

    _version_ids = [25, 26]
    _version_identifiers = ["omega-ruby", "alpha-sapphire"]
    _version_names = [
        {9: "Omega Ruby"},
        {9: "Alpha Sapphire"},
    ]

    _pokedex_ids = [15]
    _pokedex_identifiers = ["updated-hoenn"]
    _pokedex_names = [{9: ("New Hoenn", "")}]

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
    _special_tutors = [
        # fmt: off
        [450, 343, 162, 530, 324, 442, 402, 529, 340, 67, 441, 253, 9, 7, 8],
        [277, 335, 414, 492, 356, 393, 334, 387, 276, 527, 196, 401, -399, 428, 406, 304, 231],
        [20, 173, 282, 235, 257, 272, 215, 366, 143, 220, 202, 409, -355, 264, 351, 352],
        [380, 388, 180, 495, 270, 271, 478, 472, 283, 200, 278, 289, 446, -214, 285],
    ]
    _hardcode_tutors = {
        648: 547,  # meloetta / relic-song
        10018: 547,  # meloetta-pirouette / relic-song
        647: 548,  # keldeo / secret-sword
        10024: 548,  # keldeo-resolute / secret-sword
    }

    def __init__(self, sections: list) -> None:
        self._path = PATHS["omegaruby"]
        self._format = "oras"

        self._form_names["pikachu"] = [
            # TODO: check if the order is correct
            "",
            "rock-star",
            "belle",
            "pop-star",
            "phd",
            "libre",
            "cosplay",
        ]

        super().__init__(sections)
