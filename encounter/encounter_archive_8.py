from __future__ import annotations

from utils import fbs_read_as_int, fbs_read_as_vector, fbs_table


class EncounterArchive8:
    def __init__(self, data: bytes) -> None:
        self._tab = fbs_table(data)

        self.field00 = fbs_read_as_int(4, self._tab, 4)
        self.encounter_tables = fbs_read_as_vector(EncounterTable8, 4, self._tab, 6)


class EncounterTable8:
    def __init__(self, data: bytes, pos: int) -> None:
        self._tab = fbs_table(data, pos)

        self.zone_id = fbs_read_as_int(8, self._tab, 4)
        self.sub_tables = fbs_read_as_vector(EncounterSubTable8, 4, self._tab, 6)


class EncounterSubTable8:
    def __init__(self, data: bytes, pos: int) -> None:
        self._tab = fbs_table(data, pos)

        self.level_min = fbs_read_as_int(1, self._tab, 4)
        self.level_max = fbs_read_as_int(1, self._tab, 6)
        self.slots = fbs_read_as_vector(EncounterSlot8, 4, self._tab, 8)


class EncounterSlot8:
    def __init__(self, data: bytes, pos: int) -> None:
        self._tab = fbs_table(data, pos)

        self.probability = fbs_read_as_int(1, self._tab, 4)
        self.species = fbs_read_as_int(4, self._tab, 6)
        self.form = fbs_read_as_int(1, self._tab, 8)
