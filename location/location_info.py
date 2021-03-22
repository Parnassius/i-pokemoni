from __future__ import annotations

from base import BaseInfo


class LocationInfo(BaseInfo):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

