from __future__ import annotations

from base import BaseInfo
from utils import read_as_int


class EggMoveInfo(BaseInfo):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.form_table_index: int
        self.moves: list[int]
