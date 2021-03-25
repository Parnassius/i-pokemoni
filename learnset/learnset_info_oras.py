from __future__ import annotations

from os.path import join

from utils import read_as_int

from .learnset_info_xy import LearnsetInfoXY


class LearnsetInfoOrAs(LearnsetInfoXY):
    _PATH = join("a", "1", "9", "1")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
