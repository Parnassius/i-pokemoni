from __future__ import annotations

from os.path import join

from utils import read_as_int

from .machine_info import MachineInfo


class MachineInfoLetsGo(MachineInfo):
    _TYPE = "nso_ro"
    _SIZE = 2
    _MAX_ID = 59
    _SEARCH_PATTERN = bytes(
        [
            # fmt: off
            0xA0, 0x01, 0xA1, 0x01, 0xA2, 0x01, 0xA3, 0x01,
            0x6A, 0x02, 0x6B, 0x02, 0x6C, 0x02, 0xB2, 0x02,
            0xB3, 0x02, 0xB4, 0x02, 0xB5, 0x02, 0xB6, 0x02,
        ]
    )
    _SEARCH_OFFSET = 0x200_000
    _PATH = join("..", "ExeFS", "main")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.machine_number = id + 1
        self.machine_name = f"tm{self.machine_number:0>2}"
        self.move_id = read_as_int(2, self._data)
