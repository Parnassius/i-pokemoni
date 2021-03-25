from __future__ import annotations

from os.path import join

from utils import read_as_int

from .learnset_info_oras import LearnsetInfoOrAs


class LearnsetInfoSM(LearnsetInfoOrAs):
    _PATH = join("a", "0", "1", "3")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
