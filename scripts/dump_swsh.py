from __future__ import annotations

from paths import PATHS

from .dump_base import DumpBase


class DumpSwSh(DumpBase):
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
    _identifier_overrides_game_index = {
        121: "pokemon-box",
    }

    _new_item_categories = {
        49: (
            "dynamax-crystals",
            1,
            {
                9: "Dynamax crystals",
            },
        ),
        50: (
            "nature-mints",
            2,
            {
                9: "Nature mints",
            },
        ),
        51: (
            "curry-ingredients",
            1,
            {
                9: "Curry ingredients",
            },
        ),
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

    _type_tutors = [
        520,  # grass-pledge
        519,  # fire-pledge
        518,  # water-pledge
        338,  # frenzy-plant
        307,  # blast-burn
        308,  # hydro-cannon
        434,  # draco-meteor
        796,  # steel-beam
    ]
    _special_tutors = [
        [
            805,  # terrain-pulse
            807,  # burning-jealousy
            812,  # flip-turn
            804,  # rising-voltage
            803,  # grassy-glide
            813,  # triple-axel
            811,  # coaching
            810,  # corrosive-gas
            815,  # scorching-sands
            814,  # dual-wingbeat
            797,  # expanding-force
            806,  # skitter-smack
            800,  # meteor-beam
            809,  # poltergeist
            799,  # scale-shot
            808,  # lash-out
            798,  # steel-roller
            802,  # misty-explosion
        ]
    ]

    def __init__(self) -> None:
        self._path = PATHS["sword"]
        self._format = "swsh"

        super().__init__()
