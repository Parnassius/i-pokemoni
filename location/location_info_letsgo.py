from __future__ import annotations

import pickle
import re
import struct
import glob
from os.path import join, basename
from typing import cast

from base import BaseTable, T
from container.gfpack import GFPack
from text.text_file import TextFile
from utils import read_as_int

from .location_info import LocationInfo


def foo(cls_: type[T], table_: BaseTable) -> list[T]:
    table = []

    path = join(table_._path, "bin", "archive", "field")

    #files = [basename(i) for i in glob.glob(join(glob.escape(path), "*.gfpak"))]
    files = [basename(i) for i in glob.glob(join(glob.escape(path), "forest.gfpak"))]

    for filename in files:
        pack = GFPack(join(path, filename))

        for i in pack.decompressed_files:
            if b'forest' in i:
                print(i)
        print(filename)
        exit()

    return

    pack = GFPack(path)

    games = ["p", "e"]

    for game_id, game in enumerate(games):
        with open(path.format(game=game), "rb") as f:
            data = EncounterArchive7b(f.read())

        methods = {"ground", "water", "old_rod", "good_rod", "super_rod", "sky"}
        n = 0
        for encounter_table in data.encounter_tables:
            for method in methods:
                for slot in getattr(encounter_table, method)["table"]:
                    if not slot.species:
                        continue
                    table.append(
                        cls_(
                            table_,
                            table_._path,
                            n,
                            pickle.dumps((game_id, encounter_table, method, slot)),
                        )
                    )
                    n += 1

    return table


class LocationInfoLetsGo(LocationInfo):
    _CUSTOM_FUNCTION = foo

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._data = pickle.loads(data)
