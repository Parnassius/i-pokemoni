from __future__ import annotations

from os.path import join

from utils import read_as_int

from .egg_move_info import EggMoveInfo


class EggMoveInfoSM(EggMoveInfo):
    _TYPE = "garc"
    _PATH = join("a", "0", "1", "2")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.moves = []
        if len(self._data) < 2 or len(self._data) % 2 != 0:
            return

        self.form_table_index = read_as_int(2, self._data, 0)

        count = read_as_int(2, self._data, 2)
        for i in range(count):
            self.moves.append(read_as_int(2, self._data, 4 + (i * 2)))
