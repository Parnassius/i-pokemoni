from __future__ import annotations

from os.path import join

from utils import read_as_int

from .move_info_sm import MoveInfoSM


class MoveInfoUsUm(MoveInfoSM):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
