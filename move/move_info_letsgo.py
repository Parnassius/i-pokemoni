from __future__ import annotations

from os.path import join

from utils import read_as_int

from .move_info_usum import MoveInfoUsUm


class MoveInfoLetsGo(MoveInfoUsUm):
    _SIZE = 0x28
    _TYPE = "mini"
    _PATH = join("bin", "pokelib", "waza", "waza_data.bin")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
