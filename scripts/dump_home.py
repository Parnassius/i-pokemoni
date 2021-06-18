from __future__ import annotations

from paths import PATHS
from utils import adjust_stat_id

from .dump_base import DumpBase


class DumpHome(DumpBase):
    _SECTIONS = [
        "dex-xy",
        "dex-oras",
        "dex-sm",
        "dex-usum",
        "dex-letsgo",
        "dex-swsh",
        "dex-orasnx",
        "colors",
        "natures",
        "characteristics",
        "types",
    ]

    def __init__(self, sections: list) -> None:
        self._path = PATHS["home"]
        self._format = "home"

        super().__init__(sections)

    def _dump_stuff(self) -> None:
        for i in self._sections:
            if i[:4] == "dex-":
                self._dump_flavor_text(i[4:])

        if "colors" in self._sections:
            self._dump_pokemon_colors()

        if "natures" in self._sections:
            self._dump_natures()

        if "characteristics" in self._sections:
            self._dump_characteristics()

        if "types" in self._sections:
            self._dump_types()

    def _dump_flavor_text(self, game_id: str) -> None:
        games: dict[str, dict[str, int | tuple[int, ...]]] = {
            "xy": {"x": 23, "y": 24},
            "oras": {"omega": 25, "alpha": 26},
            "sm": {"sun": 27, "moon": 28},
            "usum": {"ultrasun": 29, "ultramoon": 30},
            "letsgo": {"letsgo": (31, 32)},
            "swsh": {"sword": 33, "shield": 34},
            "orasnx": {"omega_nx": 25, "alpha_nx": 26},
        }
        pokemon_species_flavor_text_csv = self._open_csv("pokemon_species_flavor_text")
        for version_name, version_ids in games[game_id].items():
            if isinstance(version_ids, int):
                version_ids = (version_ids,)
            lang_flavor_text = self._open_text_files(f"zukan_comment_{version_name}")
            for language_id, flavor_text in lang_flavor_text.items():
                for key, flavor in flavor_text:
                    parts = key.split("_")
                    pokemon_id = int(parts[2])
                    forme_id = int(parts[3])
                    if forme_id != 0:
                        continue
                    for version_id in version_ids:
                        pokemon_species_flavor_text_csv.set_row(
                            species_id=pokemon_id,
                            version_id=version_id,
                            language_id=language_id,
                            flavor_text=flavor,
                        )
                        if not flavor.strip():
                            del pokemon_species_flavor_text_csv.entries[
                                pokemon_id, version_id, language_id
                            ]

    def _dump_pokemon_colors(self) -> None:
        mappings = {  # game_id: veekun_id
            1: 8,
            2: 2,
            3: 5,
            4: 10,
            5: 6,
            6: 7,
            7: 3,
            8: 4,
            9: 9,
            10: 1,
        }
        pokemon_color_names_csv = self._open_csv("pokemon_color_names")
        lang_colors = self._open_text_files("zukan_system")
        for language_id, colors in lang_colors.items():
            for key, color in colors:
                if key[:15] == "nx_zukan_color_":
                    pokemon_color_names_csv.set_row(
                        pokemon_color_id=mappings[int(key[15:])],
                        local_language_id=language_id,
                        name=color,
                    )

    def _dump_natures(self) -> None:
        natures_csv = self._open_csv("natures")
        nature_names_csv = self._open_csv("nature_names")
        lang_natures = self._open_text_files("seikaku")
        for language_id, natures in lang_natures.items():
            for key, nature in natures:
                if nature[0] == "[":
                    continue
                game_index = int(key[-3:])
                nature_id = next(
                    i["id"]
                    for i in natures_csv.entries.values()
                    if int(i["game_index"]) == game_index
                )
                nature_names_csv.set_row(
                    nature_id=nature_id, local_language_id=language_id, name=nature
                )

    def _dump_characteristics(self) -> None:
        characteristics_csv = self._open_csv("characteristics")
        characteristic_text_csv = self._open_csv("characteristic_text")
        lang_characteristics = self._open_text_files("trainermemo")
        for language_id, characteristics in lang_characteristics.items():
            for key, characteristic in characteristics:
                if key[:10] == "trmemo_03_":
                    parts = key.split("_")
                    stat_id = adjust_stat_id(parts[2])
                    gene_mod_5 = int(parts[3])
                    characteristic_id = next(
                        i["id"]
                        for i in characteristics_csv.entries.values()
                        if int(i["stat_id"]) == stat_id
                        and int(i["gene_mod_5"]) == gene_mod_5
                    )
                    if characteristic[:16] == "Characteristic: ":
                        characteristic = characteristic[16:]
                    if characteristic[-1:] in ".。":
                        characteristic = characteristic[:-1]
                    characteristic_text_csv.set_row(
                        characteristic_id=characteristic_id,
                        local_language_id=language_id,
                        message=characteristic,
                    )

    def _dump_types(self) -> None:
        type_names_csv = self._open_csv("type_names")
        lang_types = self._open_text_files("typename")
        for language_id, types in lang_types.items():
            for key, type_ in types:
                type_id = int(key[-3:])
                if type_id < 9:
                    type_id += 1
                type_names_csv.set_row(
                    type_id=type_id, local_language_id=language_id, name=type_
                )
