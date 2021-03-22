from __future__ import annotations

from base import BaseInfo


class EncounterInfo(BaseInfo):
    _AREAS: dict[int, str | tuple[str, int]]

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.game_id: int
        self.zone_id: int
        self.level_min :int
        self.level_max :int
        self.probability :int
        self.species :int
        self.form :int


    @property
    def location_area(self) -> tuple[str, int]:
        area = self._AREAS[self.zone_id]
        if isinstance(area, str):
            area = (area, 1)
        return area

