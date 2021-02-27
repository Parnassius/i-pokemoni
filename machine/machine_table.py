from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .machine_info import MachineInfo
from .machine_info_letsgo import MachineInfoLetsGo
from .machine_info_swsh import MachineInfoSwSh


class MachineTable(BaseTable[MachineInfo]):
    _CLASSES: Mapping[str, type[MachineInfo]] = {
        "letsgo": MachineInfoLetsGo,
        "swsh": MachineInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
