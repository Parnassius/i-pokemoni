from __future__ import annotations

from paths import PATHS

from .dump_base import DumpBase


class DumpSwSh(DumpBase):
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


# TODO
# pokemon_evolution                     # evolution methods


# pokemon_moves                         # learnsets
# pokemon_items                         # wild held items

# moves SON TROPPI GUARDA DOPO
# machines                              # tr?
# locations/location_names
# location_areas/location_area_prose


# items/item_names/item_prose/item_flavor_text
# item_game_indices
# item_flag_map
# item_categories

# encounters SON TROPPI GUARDA DOPO
