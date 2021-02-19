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


class DumpLetsGo(DumpBase):
    def __init__(self) -> None:
        self.path = PATHS["pikachu"]
        self.file_format = "letsgo"

        super().__init__()
