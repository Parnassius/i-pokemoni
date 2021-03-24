from __future__ import annotations

from os.path import join

from utils import read_as_int

from .egg_move_info_sm import EggMoveInfoSM


class EggMoveInfoUsUm(EggMoveInfoSM):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
