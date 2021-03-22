from __future__ import annotations

from collections.abc import Mapping

from base import BaseTable

from .location_info import LocationInfo
from .location_info_letsgo import LocationInfoLetsGo
from .location_info_swsh import LocationInfoSwSh


class LocationTable(BaseTable[LocationInfo]):
    _CLASSES: Mapping[str, type[LocationInfo]] = {
        "letsgo": LocationInfoLetsGo,
        "swsh": LocationInfoSwSh,
    }

    def __init__(self, path: str, file_format: str) -> None:
        super().__init__(path, file_format)
