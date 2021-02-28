from __future__ import annotations

from os.path import join

from utils import read_as_int

from .egg_move_info import EggMoveInfo


class EggMoveInfoSwSh(EggMoveInfo):
    _TYPE = "multiplefiles"
    _MAX_ID = 1250
    _PATH = join("bin", "pml", "tamagowaza", "tamagowaza_{id:0>4}.bin")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.form_table_index = read_as_int(2, self._data, 0, True)

        count = read_as_int(2, self._data, 2, True)
        self.moves = []
        for i in range(count):
            self.moves.append(read_as_int(2, self._data, 4 + (i * 2), True))
