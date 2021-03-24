from __future__ import annotations

from os.path import join

from utils import read_as_int

from .learnset_info_usum import LearnsetInfoUsUm


class LearnsetInfoLetsGo(LearnsetInfoUsUm):
    _TYPE = "gfpak"
    _PATH = join("bin", "archive", "waza_oboe.gfpak")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)
