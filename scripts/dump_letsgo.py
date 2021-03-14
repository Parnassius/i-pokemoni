from __future__ import annotations

from paths import PATHS

from .dump_base import DumpBase


class DumpLetsGo(DumpBase):
    _SECTIONS = [
        "moves",
        "abilities",
        "items",
        "machines",
        "pokemon",
        "locations",
    ]

    _changed_items = {
        113: 555,  # tea
        123: 550,  # tm-case
        874: 548,  # silph-scope
        877: 546,  # gold-teeth
        878: 547,  # lift-key
    }

    _new_item_categories = {
        47: (
            "species-candies",
            1,
            {
                9: "Species candies",
            },
        ),
        48: (
            "catching-bonus",
            5,
            {
                9: "Catching bonus",
            },
        ),
    }

    _locations_script = False
    _locations_subtitle = False
    _locations_areas_names = {
        "mt-moon": ["1F", "B1F", "B2F"],
        "rock-tunnel": ["1F", "B1F"],
        "seafoam-islands": ["1F", "B1F", "B2F", "B3F", "B3F-bis", "B4F", "B4F-bis"],
        "kanto-victory-road-2": ["1F", "2F", "3F"],
        "kanto-route-2": ["south, towards Viridian City", "north, towards Pewter City"],
        "kanto-route-4": ["", "Pokemon Center"],
        "kanto-route-10": ["", ""],  # TODO
        "kanto-route-11": ["", ""],  # TODO
        "kanto-route-15": ["", ""],  # TODO
        "kanto-route-16": ["", ""],  # TODO
        "kanto-route-18": ["", ""],  # TODO
        "kanto-route-20": ["", ""],  # TODO maybe?
        "cerulean-cave": ["1F", "2F", "B1F"],
        "pokemon-tower": ["3F", "4F", "5F", "6F"],
        "pokemon-mansion": ["1F", "2F", "3F", "B1F"],
    }

    _region_id = 1
    _region_identifier = "kanto"
    _region_names = {9: "Kanto"}

    _generation_id = 7
    _generation_identifier = "generation-vii"
    _generation_main_region = 7
    _generation_names = {9: "Generation VII"}

    _version_group_id = 19
    _version_group_identifier = "lets-go-pikachu-lets-go-eevee"
    _version_group_order = 19

    _version_ids = [31, 32]
    _version_identifiers = ["lets-go-pikachu", "lets-go-eevee"]
    _version_names = [  # bin/messages/*/common/pmgo_set.dat
        {9: "Let’s Go, Pikachu!"},
        {9: "Let’s Go, Eevee!"},
    ]

    _pokedex_ids = [26]
    _pokedex_identifiers = ["letsgo-kanto"]
    _pokedex_names = [
        {9: ("Let’s Go Kanto", "Let’s Go: Pikachu/Let’s Go: Eevee Kanto dex")}
    ]

    _single_flavor_text = True

    _type_tutors = [0] * 32
    _special_tutors = [
        [
            729,  # zippy-zap
            731,  # floaty-fall
            730,  # splishy-splash
            733,  # bouncy-bubble
            734,  # buzzy-buzz
            735,  # sizzly-slide
            736,  # glitzy-glow
            737,  # baddy-bad
            738,  # sappy-seed
            739,  # freezy-frost
            740,  # sparkly-swirl
        ]
    ]

    def __init__(self, sections: list) -> None:
        self._path = PATHS["pikachu"]
        self._format = "letsgo"

        super().__init__(sections)
