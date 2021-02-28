from __future__ import annotations

import re
import struct
from os.path import join

from base import BaseTable, T
from text.text_file import TextFile
from utils import read_as_int

from .machine_info import MachineInfo


def match_machine_move(cls_: type[T], table_: BaseTable) -> list[T]:
    table = []

    item_names = [
        (int(k[k.find("_") + 1 :]), v)
        for k, v in TextFile(table_._path, "English", "itemname", "swsh").lines
        if re.match(r"^T[RM]\d\d$", v)
    ]
    # item_names.sort(key=lambda x: (x[1][:2], x[1][2:] == "00", x[1][2:]))
    item_names.sort(key=lambda x: x[1])
    languages = [
        "JPN",
        "Korean",
        "Trad_Chinese",
        "French",
        "German",
        "Spanish",
        "Italian",
        "English",
        "JPN_KANJI",
        "Simp_Chinese",
    ]
    item_descriptions = {}
    move_descriptions = {}
    for lang in languages:
        item_descriptions[lang] = {
            int(k[k.find("_") + 1 :]): v
            for k, v in TextFile(table_._path, lang, "iteminfo", "swsh").lines
        }
        move_descriptions[lang] = [
            (int(k[k.find("_") + 1 :]), v)
            for k, v in TextFile(table_._path, lang, "wazainfo", "swsh").lines
        ]

    n = 0
    for item_name in item_names:
        for lang in languages:
            item_desc = item_descriptions[lang][item_name[0]]
            moves = [k for k, v in move_descriptions[lang] if v == item_desc]
            if len(moves) == 1:
                move_id = moves[0]
                break
        else:
            if item_name[1] == "TR22":
                move_id = 188  # sludge-bomb
            elif item_name[1] == "TR25":
                move_id = 473  # psyshock
            else:
                print(item_name[1], moves)
                continue

        table.append(cls_(table_, table_._path, n, struct.pack("<H", move_id)))
        n += 1

    return table


class MachineInfoSwSh(MachineInfo):
    _CUSTOM_FUNCTION = match_machine_move

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.machine_number = id + 1
        machine_type = "tm" if self.machine_number <= 100 else "tr"
        self.machine_name = f"{machine_type}{str(self.machine_number)[-2:]:0>2}"
        self.move_id = read_as_int(2, self._data)
