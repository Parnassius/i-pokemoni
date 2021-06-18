from __future__ import annotations

from os.path import join

from paths import PATHS
from utils import read_as_int

from .dump_base import DumpBase


class DumpUsUm(DumpBase):
    _SECTIONS = ["moves", "learnsets", "pokemon"]

    _region_id = 7
    _region_identifier = "alola"
    _region_names = {9: "Alola"}

    _generation_id = 7
    _generation_identifier = "generation-vii"
    _generation_main_region = 7
    _generation_names = {9: "Generation VII"}

    _version_group_id = 18
    _version_group_identifier = "ultra-sun-ultra-moon"
    _version_group_order = 18

    _version_ids = [29, 30]
    _version_identifiers = ["ultra-sun", "ultra-moon"]
    _version_names = [
        {9: "Ultra Sun"},
        {9: "Ultra Moon"},
    ]

    _pokedex_ids = [21, 22, 23, 24, 25]
    _pokedex_identifiers = [
        "updated-alola",
        "updated-melemele",
        "updated-akala",
        "updated-ulaula",
        "updated-poni",
    ]
    _pokedex_names = [
        {9: ("Updated Alola", "")},
        {9: ("Updated Melemele", "")},
        {9: ("Updated Akala", "")},
        {9: ("Updated Ula'ula", "")},
        {9: ("Updated Poni", "")},
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
    _special_tutors = [
        [
            450,
            343,
            162,
            530,
            324,
            442,
            402,
            529,
            340,
            67,
            441,
            253,
            9,
            7,
            8,
            277,
            335,
            414,
            492,
            356,
            393,
            334,
            387,
            276,
            527,
            196,
            401,
            428,
            406,
            304,
            231,
            20,
            173,
            282,
            235,
            257,
            272,
            215,
            366,
            143,
            220,
            202,
            409,
            264,
            351,
            352,
            380,
            388,
            180,
            495,
            270,
            271,
            478,
            472,
            283,
            200,
            278,
            289,
            446,
            285,
            477,
            502,
            432,
            710,
            707,
            675,
            673,
        ]
    ]
    _hardcode_tutors = {
        648: 547,  # meloetta / relic-song
        10018: 547,  # meloetta-pirouette / relic-song
        647: 548,  # keldeo / secret-sword
        10024: 548,  # keldeo-resolute / secret-sword
        25: 344,  # pikachu / volt-tackle
    }

    def __init__(self, sections: list) -> None:
        self._path = PATHS["ultrasun"]
        self._format = "usum"

        """with open(join(self._path, 'Shop.cro'), 'rb') as f:
            f.seek(0x52d2)
            move_counts = [read_as_int(1, f) for _ in range(4)]
            f.seek(0x54DE)
            for count in move_counts:
                tutors = []
                for i in range(count):
                    tutors.append(read_as_int(2, f))
                    f.seek(2, 1)  # cost
                self._special_tutors.append(tutors)"""

        super().__init__(sections)
