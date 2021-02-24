from __future__ import annotations

from os.path import join

from utils import read_as_int

from .learnset_info import LearnsetInfo


class LearnsetInfoSwSh(LearnsetInfo):
    _SIZE = 0x104
    _TYPE = "singlefile_noheader"
    _PATH = join("bin", "pml", "waza_oboe", "wazaoboe_total.bin")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.moves = []
        pos = 0
        while pos < self._SIZE:
            # check 3rd byte of each u16/u16 tuple, level is never > 255
            if self._data[pos + 3] == 0xFF:
                break
            self.moves.append(
                (
                    read_as_int(2, self._data, pos, True),
                    read_as_int(2, self._data, pos + 2, True),
                )
            )
            pos += 4
