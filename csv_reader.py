from __future__ import annotations

import csv
from collections.abc import Sequence
from copy import copy
from os.path import dirname, join
from typing import Literal


class CsvReader:
    def __init__(self, table: str) -> None:
        self.table = table
        self.file = join(dirname(__file__), "veekun", f"{self.table}.csv")
        self.primary_key = {
            "ability_flavor_text": (0, 1, 2),
            "ability_names": (0, 1),
            "evolution_trigger_prose": (0, 1),
            "generation_names": (0, 1),
            "item_category_prose": (0, 1),
            "item_flavor_text": (0, 1, 2),
            "item_game_indices": (0, 1),
            "item_names": (0, 1),
            "location_area_prose": (0, 1),
            "location_names": (0, 1),
            "machines": (0, 1),
            "move_changelog": (0, 1),
            "move_effect_prose": (0, 1),
            "move_flag_map": (0, 1),
            "move_flavor_text": (0, 1, 2),
            "move_meta_ailment_names": (0, 1),
            "move_meta_category_prose": (0, 1),
            "move_names": (0, 1),
            "move_meta_stat_changes": (0, 1),
            "pokedex_prose": (0, 1),
            "pokedex_version_groups": (0, 1),
            "pokemon_abilities": (0, 3),
            "pokemon_dex_numbers": (0, 1),
            "pokemon_egg_groups": (0, 1),
            "pokemon_form_generations": (0, 1),
            "pokemon_form_names": (0, 1),
            "pokemon_moves": (0, 1, 2, 3, 4),
            "pokemon_species_flavor_text": (0, 1, 2),
            "pokemon_species_names": (0, 1),
            "pokemon_stats": (0, 1),
            "pokemon_types": (0, 2),
            "region_names": (0, 1),
            "version_group_regions": (0, 1),
            "version_names": (0, 1),
        }.get(table, (0,))

        with open(self.file, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            self.header = tuple(next(reader))
            self.entries = {}
            for row in reader:
                key = self._get_primary_key(row)
                self.entries[key] = dict(zip(self.header, row))

    def _get_primary_key(
        self, row: Sequence[int | str] | dict[str, int | str]
    ) -> tuple[int | str, ...]:
        if isinstance(row, dict):
            row = [row.get(i, "") for i in self.header]
        key: list[int | str] = []
        for col in self.primary_key:
            if isinstance(col, int):
                key.append(int(row[col]))
            else:
                key.append(row[int(col)])
        return tuple(key)

    def set_row(self, **val: int | str | Literal[False]) -> None:
        key = self._get_primary_key(val)
        if key not in self.entries:
            self.entries[key] = {
                i: str(val.get(i + "_fallback_", "")) for i in self.header
            }

        self.entries[key].update(
            {
                k: str(v)
                for k, v in val.items()
                if not k.endswith("_fallback_") and v is not False
            }
        )

    def save(self) -> None:
        with open(self.file, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",", lineterminator="\n")
            writer.writerow(self.header)
            writer.writerows([i[1].values() for i in sorted(self.entries.items())])
