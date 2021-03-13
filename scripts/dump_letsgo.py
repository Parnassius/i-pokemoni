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
