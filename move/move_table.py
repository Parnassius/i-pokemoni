from __future__ import annotations

from collections.abc import Sequence
from os.path import join
from typing import Literal, overload

from utils import read_as_int, read_mini

from .move_info import MoveInfo
from .move_info_letsgo import MoveInfoLetsGo
from .move_info_swsh import MoveInfoSwSh


class MoveTable:
    def __init__(self, path: str, file_format: str) -> None:
        self._MoveInfo: type[MoveInfo] = {
            "letsgo": MoveInfoLetsGo,
            "swsh": MoveInfoSwSh,
        }[file_format]
        self._path = path
        self._format = file_format
        self._size = self._MoveInfo._SIZE

        self._table = []
        if self._size is None:  # different file for each move
            for move_id in range(self._MoveInfo._MAX_MOVE_ID + 1):
                with open(
                    join(path, self._MoveInfo._PATH.format(move_id=move_id)), "rb"
                ) as f:
                    self._table.append(self._MoveInfo(self, path, move_id, f.read()))
        else:  # single file
            with open(join(path, self._MoveInfo._PATH), "rb") as f:
                self._data = f.read()
            for move_id, move_data in enumerate(read_mini(self._data)):
                self._table.append(self._MoveInfo(self, path, move_id, move_data))

    def get_move_info(self, index: int) -> MoveInfo:
        return self._table[index]

    @overload
    @classmethod
    def get(cls, path: str, file_format: Literal["letsgo"]) -> list[MoveInfoLetsGo]:
        ...

    @overload
    @classmethod
    def get(cls, path: str, file_format: Literal["swsh"]) -> list[MoveInfoSwSh]:
        ...

    # suppress "Overloaded function implementation cannot produce return type ..."
    @classmethod  # type: ignore[misc]
    def get(cls, path: str, file_format: str) -> Sequence[MoveInfo]:
        return cls(path, file_format)._table
