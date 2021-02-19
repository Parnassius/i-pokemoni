from __future__ import annotations

from os.path import join
from typing import Literal
from evolution.evolution_set import Evolution
from csv_reader import CsvReader
from paths import PATHS
from personal.personal_info import PersonalInfo
from personal.personal_table import PersonalTable
from item.item_table import ItemTable
from text.text_file import TextFile
from utils import to_id


from .base import DumpBase


class DumpSwSh(DumpBase):
    def __init__(self) -> None:
        self.path = PATHS["sword"]
        self.file_format = "swsh"

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
