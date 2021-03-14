from __future__ import annotations

import re
import struct
from os.path import join

from base import BaseTable, T
from container.gfpack import GFPack
from text.text_file import TextFile
from utils import read_as_int

from .encounter_archive_8 import EncounterArchive8
from .encounter_info import EncounterInfo


def foo(cls_: type[T], table_: BaseTable) -> list[T]:
    table: list[T] = []

    path = join(table_._path, "bin", "archive", "field", "resident", "data_table.gfpak")

    print(path)

    pack = GFPack(path)

    symbols_sw = EncounterArchive8(pack.get_data_file_name("encount_symbol_k.bin"))
    hidden_sw = EncounterArchive8(pack.get_data_file_name("encount_k.bin"))
    symbols_sh = EncounterArchive8(pack.get_data_file_name("encount_symbol_t.bin"))
    hidden_sh = EncounterArchive8(pack.get_data_file_name("encount_t.bin"))

    for encounter_table in hidden_sw.encounter_tables:
        """
        Clear
        Cloudy
        Rain
        Thunderstorm
        Harsh sunlight
        Snow
        Blizzard
        Sandstorm
        Fog
        """
        for sub_table in encounter_table.sub_tables:
            for slot in sub_table.slots:
                if (
                    encounter_table.zone_id == 0x77677B717EA450BD
                    and slot.probability == 40
                ):
                    print(
                        symbols_sw.field00,
                        sub_table.level_min,
                        sub_table.level_max,
                        slot.species,
                        slot.form,
                    )

    exit()

    return table


class EncounterInfoSwSh(EncounterInfo):
    _TYPE = "gfpak"
    _SIZE = 2
    _MAX_ID = 59
    _PATH = join("bin", "archive", "field", "resident", "data_table.gfpak")

    _CUSTOM_FUNCTION = foo

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
