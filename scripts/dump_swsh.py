from __future__ import annotations

from paths import PATHS

from .dump_base import DumpBase


class DumpSwSh(DumpBase):
    _new_items = set(range(1074, 1607 + 1))

    _changed_items = {
        121: 1007,  # pokemon-box => pokemon-box-link
        252: 229,  # up-grade => upgrade
        259: 236,  # stick => leek
        565: 606,  # health-wing => health-feather
        566: 607,  # muscle-wing => muscle-feather
        567: 608,  # resist-wing => resist-feather
        568: 609,  # genius-wing => genius-feather
        569: 610,  # clever-wing => clever-feather
        570: 611,  # swift-wing => swift-feather
        571: 612,  # pretty-wing => pretty-feather
        703: 732,  # adventure-rules => adventure-guide
    }

    _new_evolution_methods = {
        5: (
            "spin",
            {
                9: "Spin",
            },
        ),
        6: (
            "tower-of-darkness",
            {
                9: "Train in the Tower of Darkness",
            },
        ),
        7: (
            "tower-of-waters",
            {
                9: "Train in the Tower of Waters",
            },
        ),
    }

    _new_move_meta_ailments = {
        42: (
            "tar-shot",
            {
                9: "Tar shot",
            },
        ),
    }

    _region_id = 8
    _region_identifier = "galar"
    _region_names = {9: "Galar"}

    _generation_id = 8
    _generation_identifier = "generation-viii"
    _generation_main_region = 8
    _generation_names = {9: "Generation VIII"}

    _version_group_id = 20
    _version_group_identifier = "sword-shield"
    _version_group_order = 20

    _version_ids = [33, 34]
    _version_identifiers = ["sword", "shield"]
    _version_names = [
        {9: "Sword"},
        {9: "Shield"},
    ]

    _pokedex_ids = [27, 28, 29]
    _pokedex_identifiers = ["galar", "isle-of-armor", "crown-tundra"]
    _pokedex_names = [
        {9: ("Galar", "")},
        {9: ("Isle of Armor", "")},
        {9: ("Crown Tundra", "")},
    ]

    def __init__(self) -> None:
        self._path = PATHS["sword"]
        self._format = "swsh"

        super().__init__()
