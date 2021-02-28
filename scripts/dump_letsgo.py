from __future__ import annotations

from paths import PATHS

from .dump_base import DumpBase


class DumpLetsGo(DumpBase):
    _new_items = {
        115,
        121,
        122,
        124,
        125,
        126,
        127,
        128,
        872,
        873,
        875,
        876,
        900,
        901,
        902,
        903,
    }
    _new_items.update(range(861, 866 + 1))
    _new_items.update(range(885, 896 + 1))
    _new_items.update(range(960, 1057 + 1))
    _changed_items = {
        113: 555,  # tea
        123: 550,  # tm case
        873: 433,  # ss-ticket
        874: 548,  # silph-scope
        875: 436,  # parcel
        876: 475,  # card-key
        877: 546,  # gold-teeth
        878: 547,  # lift-key
        947: 993,  # ilima-normalium-z
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

    def __init__(self) -> None:
        self._path = PATHS["pikachu"]
        self._format = "letsgo"

        super().__init__()
