from __future__ import annotations

from os.path import join
from typing import Any, Callable

from utils import read_as_int

from .egg_move_info import EggMoveInfo


class EggMoveInfoLetsGo(EggMoveInfo):
    _SKIP = True

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
