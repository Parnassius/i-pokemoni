from __future__ import annotations

from os.path import join

from utils import read_as_int

from .learnset_info import LearnsetInfo


class LearnsetInfoXY(LearnsetInfo):
    _TYPE = "garc"
    _PATH = join("a", "2", "1", "4")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.moves = []
        if len(self._data) < 4 or len(self._data) % 4 != 0:
            return

        pos = 0
        for i in range((len(data) // 4) - 1):
            self.moves.append(
                (
                    read_as_int(2, self._data, pos, True),
                    read_as_int(2, self._data, pos + 2, True),
                )
            )
            pos += 4
