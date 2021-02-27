from __future__ import annotations

from base import BaseInfo


class MachineInfo(BaseInfo):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.machine_number: int
        self.machine_name: str
        self.move_id: int
