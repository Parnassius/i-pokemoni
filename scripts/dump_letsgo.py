from __future__ import annotations

from paths import PATHS

from .dump_base import DumpBase


class DumpLetsGo(DumpBase):
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
