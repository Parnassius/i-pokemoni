from __future__ import annotations

from utils import fbs_read_as_bool, fbs_read_as_int, fbs_read_as_vector, fbs_table


class EncounterArchive7b:
    def __init__(self, data: bytes) -> None:
        self._tab = fbs_table(data)

        self.encounter_tables = fbs_read_as_vector(EncounterTable7b, 4, self._tab, 4)


class EncounterTable7b:
    def __init__(self, data: bytes, pos: int) -> None:
        self._tab = fbs_table(data, pos)

        self.zone_id = fbs_read_as_int(8, self._tab, 4)
        self.trainer_rank_min = fbs_read_as_int(4, self._tab, 6)
        self.trainer_rank_max = fbs_read_as_int(4, self._tab, 8)

        self.ground = {
            "spawn_allowed": fbs_read_as_bool(self._tab, 10),
            "spawn_count_max": fbs_read_as_int(4, self._tab, 12),
            "spawn_duration": fbs_read_as_int(4, self._tab, 14),
            "table_encounter_rate": fbs_read_as_int(4, self._tab, 16),
            "table_level_min": fbs_read_as_int(4, self._tab, 18),
            "table_level_max": fbs_read_as_int(4, self._tab, 20),
            "table_rand_chance_total": fbs_read_as_int(4, self._tab, 22),
            "table": fbs_read_as_vector(EncounterSlot7b, 4, self._tab, 24),
        }

        self.water = {
            "spawn_allowed": fbs_read_as_bool(self._tab, 26),
            "spawn_count_max": fbs_read_as_int(4, self._tab, 28),
            "spawn_duration": fbs_read_as_int(4, self._tab, 30),
            "table_encounter_rate": fbs_read_as_int(4, self._tab, 32),
            "table_level_min": fbs_read_as_int(4, self._tab, 34),
            "table_level_max": fbs_read_as_int(4, self._tab, 36),
            "table_rand_chance_total": fbs_read_as_int(4, self._tab, 38),
            "table": fbs_read_as_vector(EncounterSlot7b, 4, self._tab, 40),
        }

        self.old_rod = {
            "table_encounter_rate": fbs_read_as_int(4, self._tab, 42),
            "table_level_min": fbs_read_as_int(4, self._tab, 44),
            "table_level_max": fbs_read_as_int(4, self._tab, 46),
            "table_rand_chance_total": fbs_read_as_int(4, self._tab, 48),
            "table": fbs_read_as_vector(EncounterSlot7b, 4, self._tab, 50),
        }

        self.good_rod = {
            "table_encounter_rate": fbs_read_as_int(4, self._tab, 52),
            "table_level_min": fbs_read_as_int(4, self._tab, 54),
            "table_level_max": fbs_read_as_int(4, self._tab, 56),
            "table_rand_chance_total": fbs_read_as_int(4, self._tab, 58),
            "table": fbs_read_as_vector(EncounterSlot7b, 4, self._tab, 60),
        }

        self.super_rod = {
            "table_encounter_rate": fbs_read_as_int(4, self._tab, 62),
            "table_level_min": fbs_read_as_int(4, self._tab, 64),
            "table_level_max": fbs_read_as_int(4, self._tab, 66),
            "table_rand_chance_total": fbs_read_as_int(4, self._tab, 68),
            "table": fbs_read_as_vector(EncounterSlot7b, 4, self._tab, 70),
        }

        self.sky = {
            "spawn_allowed": fbs_read_as_bool(self._tab, 72),
            "spawn_count_max": fbs_read_as_int(4, self._tab, 74),
            "spawn_duration": fbs_read_as_int(4, self._tab, 76),
            "table_encounter_rate": fbs_read_as_int(4, self._tab, 78),
            "table_level_min": fbs_read_as_int(4, self._tab, 80),
            "table_level_max": fbs_read_as_int(4, self._tab, 82),
            "table_rand_chance_total": fbs_read_as_int(4, self._tab, 84),
            "table": fbs_read_as_vector(EncounterSlot7b, 4, self._tab, 86),
        }


class EncounterSlot7b:
    def __init__(self, data: bytes, pos: int) -> None:
        self._tab = fbs_table(data, pos)

        self.probability = fbs_read_as_int(4, self._tab, 4, True)
        self.species = fbs_read_as_int(4, self._tab, 6, True)
        self.form = fbs_read_as_int(2, self._tab, 8, True)
