from __future__ import annotations

import pickle
import re
import struct
from os.path import join
from typing import cast

from base import BaseTable, T
from container.gfpack import GFPack
from text.text_file import TextFile
from utils import read_as_int

from .encounter_archive_7b import EncounterArchive7b
from .encounter_info import EncounterInfo


def foo(cls_: type[T], table_: BaseTable) -> list[T]:
    table = []

    path = join(
        table_._path, "bin", "field", "param", "encount", "encount_data_{game}.bin"
    )

    games = ["p", "e"]

    for game_id, game in enumerate(games):
        with open(path.format(game=game), "rb") as f:
            data = EncounterArchive7b(f.read())

        methods = {"ground", "water", "old_rod", "good_rod", "super_rod", "sky"}
        n = 0
        for encounter_table in data.encounter_tables:
            for method in methods:
                for slot in getattr(encounter_table, method)["table"]:
                    if not slot.species:
                        continue
                    table.append(
                        cls_(
                            table_,
                            table_._path,
                            n,
                            pickle.dumps((game_id, encounter_table, method, slot)),
                        )
                    )
                    n += 1

    return table


class EncounterInfoLetsGo(EncounterInfo):
    _CUSTOM_FUNCTION = foo

    _AREAS = {
        9728528903495300547: "viridian-forest",
        3485091976487167253: "mt-moon",
        3485088677952282620: ("mt-moon", 2),
        3485089777463910831: ("mt-moon", 3),
        18433398720351318102: "rock-tunnel",
        18433397620839689891: ("rock-tunnel", 2),
        1139530970275538988: "power-plant",
        11386706514488678199: "digletts-cave",
        9339305161684547019: "seafoam-islands",
        9339306261196175230: ("seafoam-islands", 2),
        9339307360707803441: ("seafoam-islands", 3),
        430105244008401104: ("seafoam-islands", 4),
        430108542543285737: ("seafoam-islands", 5),
        1140329282511499499: ("seafoam-islands", 6),
        1140330382023127710: ("seafoam-islands", 7),
        2977322004419460624: "victory-road",
        2977325302954345257: ("victory-road", 2),
        2977324203442717046: ("victory-road", 3),
        7413069074332517478: "route-1",
        18396013927812435727: "route-2",
        18396015027324063938: ("route-2", 2),
        7413066875309261056: "route-3",
        3598603922747771661: "route-4",
        3598600624212887028: ("route-4", 2),
        7413073472379030322: "route-5",
        7413072372867402111: "route-6",
        7413071273355773900: "route-7",
        7413078969937171377: "route-8",
        7413077870425543166: "route-9",
        12701893868473318500: "route-10",
        12701897167008203133: ("route-10", 2),
        13228561037752690911: "route-11",
        13228562137264319122: ("route-11", 2),
        7412221350867356022: "route-12",
        7412222450378984233: "route-13",
        7412223549890612444: "route-14",
        15824635534629551987: "route-15",
        15824636634141180198: ("route-15", 2),
        16351333490234514306: "route-16",
        16351332390722886095: ("route-16", 2),
        7412226848425497077: "route-17",
        17710521177375417420: "route-18",
        17710524475910302053: ("route-18", 2),
        7412229047448753499: "route-19",
        7415053692821059883: "route-20",
        8874646829087534634: ("route-20", 2),
        7415052593309431672: "route-21",
        7415055891844316305: "route-22",
        7415054792332688094: "route-23",
        7415058090867572727: "route-24",
        7415056991355944516: "route-25",
        209034189613473363: "cerulean-cave",
        209035289125101574: ("cerulean-cave", 2),
        209036388636729785: ("cerulean-cave", 3),
        10943373203928000592: "pokemon-tower",
        10943380900509398069: ("pokemon-tower", 2),
        10943379800997769858: ("pokemon-tower", 3),
        10943378701486141647: ("pokemon-tower", 4),
        16276526804362071941: "pokemon-mansion",
        16276523505827187308: ("pokemon-mansion", 2),
        16276524605338815519: ("pokemon-mansion", 3),
        16276521306803930886: ("pokemon-mansion", 4),
        4201142782482242836: "pallet-town",
        4201146081017127469: "viridian-city",
        4201144981505499258: "pewter-city",
        4201139483947358203: "cerulean-city",
        4201138384435729992: "lavender-town",
        4201141682970614625: "vermilion-city",
        4201135085900845359: "fuchsia-city",
        4201133986389217148: "cinnabar-island",
    }

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._data = pickle.loads(data)

        self.game_id = self._data[0]
        self._encounter_table = self._data[1]
        self.method = self._data[2]
        self._slot = self._data[3]

        self.zone_id = self._encounter_table.zone_id
        self.trainer_rank_min = self._encounter_table.trainer_rank_min
        self.trainer_rank_max = self._encounter_table.trainer_rank_max

        self._method_data = getattr(self._encounter_table, self.method)
        if not self.method.endswith("_rod"):
            self.spawn_allowed = self._method_data["spawn_allowed"]
            self.spawn_count_max = self._method_data["spawn_count_max"]
            self.spawn_duration = self._method_data["spawn_duration"]
        self.table_encounter_rate = self._method_data["table_encounter_rate"]
        self.level_min = self._method_data["table_level_min"]
        self.level_max = self._method_data["table_level_max"]
        self.table_rand_chance_total = self._method_data["table_rand_chance_total"]

        self.probability = self._slot.probability
        self.species = self._slot.species
        self.form = self._slot.form
