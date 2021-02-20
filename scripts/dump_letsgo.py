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
        861,
        862,
        863,
        864,
        865,
        866,
        885,
        886,
        887,
        888,
        889,
        890,
        891,
        892,
        893,
        894,
        895,
        896,
        900,
        901,
        902,
        903,
    }
    _new_items.update(range(960, 1057 + 1))
    _changed_items = {
        450: 919,
        713: 929,
        739: 780,
        740: 934,
        947: 993,
        943: 989,
        944: 990,
        945: 991,
        946: 992,
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

    def __init__(self) -> None:
        self._path = PATHS["pikachu"]
        self._format = "letsgo"

        super().__init__()
