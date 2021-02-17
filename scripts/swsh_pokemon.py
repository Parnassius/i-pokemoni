from __future__ import annotations

from os.path import join
from typing import Literal

from csv_reader import CsvReader
from paths import PATHS
from personal.personal_info import PersonalInfo
from personal.personal_table import PersonalTable
from text.text_file import TextFile
from utils import to_id


class SwShPokemon:
    def __init__(self) -> None:
        self.path = PATHS["sword"]

        self.form_names: dict[str, list[str | None | Literal[False]]] = {
            # fmt: off
            "pikachu": ["", "original-cap", "hoenn-cap", "sinnoh-cap", "unova-cap", "kalos-cap", "alola-cap", "partner-cap", None, "world-cap"],
            "raichu": ["", "alola"],
            "sandshrew": ["", "alola"],
            "sandslash": ["", "alola"],
            "vulpix": ["", "alola"],
            "ninetales": ["", "alola"],
            "diglett": ["", "alola"],
            "dugtrio": ["", "alola"],
            "meowth": ["", "alola", "galar"],
            "persian": ["", "alola"],
            "ponyta": ["", "galar"],
            "rapidash": ["", "galar"],
            "slowpoke": ["", "galar"],
            "slowbro": ["", "mega", "galar"],
            "farfetchd": ["", "galar"],
            "exeggutor": ["", "alola"],
            "marowak": ["", "alola"],
            "weezing": ["", "galar"],
            "mr-mime": ["", "galar"],
            "articuno": ["", "galar"],
            "zapdos": ["", "galar"],
            "moltres": ["", "galar"],
            "slowking": ["", "galar"],
            "corsola": ["", "galar"],
            "zigzagoon": ["", "galar"],
            "linoone": ["", "galar"],
            "rayquaza": [""],
            "cherrim": ["", False],
            "shellos": ["", False],
            "gastrodon": ["", False],
            "rotom": ["", "heat", "wash", "frost", "fan", "mow"],
            "giratina": ["altered", "origin"],
            "basculin": ["red-striped", "blue-striped"],
            "darumaka": ["", "galar"],
            "darmanitan": ["standard", "zen", "galar-standard", "galar-zen"],
            "yamask": ["", "galar"],
            "stunfisk": ["", "galar"],
            "tornadus": ["incarnate", "therian"],
            "thundurus": ["incarnate", "therian"],
            "landorus": ["incarnate", "therian"],
            "kyurem": ["", "white", "black"],
            "keldeo": ["ordinary", "resolute"],
            "genesect": ["", False, False, False, False],
            "meowstic": ["male", "female"],
            "aegislash": ["shield", "blade"],
            "pumpkaboo": ["average", "small", "large", "super"],
            "gourgeist": ["average", "small", "large", "super"],
            "xerneas": ["", False],
            "zygarde": ["", "10", False, "50", "Complete"],
            "rockruff": ["", "own-tempo"],
            "lycanroc": ["midday", "midnight", "dusk"],
            "wishiwashi": ["solo", "school"],
            "silvally": ["", False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            "mimikyu": ["disguised", "busted"],
            "necrozma": ["", "dusk", "dawn", "ultra"],
            "magearna": ["", "original"],
            "cramorant": ["", "gulping", "gorging"],
            "toxtricity": ["amped", "low-key"],
            "sinistea": ["", False],
            "polteageist": ["", False],
            "alcremie": ["", False, False, False, False, False, False, False, False],
            "eiscue": ["ice", "noice"],
            "indeedee": ["male", "female"],
            "morpeko": ["full-belly", "hangry"],
            "zacian": ["", "crowned"],
            "zamazenta": ["", "crowned"],
            "eternatus": ["", "eternamax"],
            "urshifu": ["single-strike", "rapid-strike"],
            "zarude": ["", "dada"],
            "calyrex": ["", "ice", "shadow"],
        }
        self.gen7 = ["meltan", "melmetal"]
        self.legendary_list = [
            # fmt: off
            "zacian", "zamazenta", "eternatus",
            "kubfu", "urshifu",
            "regieleki", "regidrago", "glastrier", "spectrier", "calyrex",
        ]
        self.mythical_list = ["zarude"]

        self.tables: dict[str, CsvReader] = {}
        self.text_files: dict[tuple[str, ...], list[tuple[str, str]]] = {}

        self.pokemon_csv = self._open_table("pokemon")
        self.pokemon_species_csv = self._open_table("pokemon_species")
        self.evolution_chains_csv = self._open_table("evolution_chains")
        self.pokemon_species_names_csv = self._open_table("pokemon_species_names")
        self.pokemon_species_flavor_text_csv = self._open_table(
            "pokemon_species_flavor_text"
        )
        self.pokemon_stats_csv = self._open_table("pokemon_stats")
        self.pokemon_types_csv = self._open_table("pokemon_types")

        self.personal_table = PersonalTable(self.path, "swsh")

        self._dump_pokemon()
        self._create_evolution_chains()
        self._update_pokemon_order()
        self._update_pokemon_species_order()

        self._save_all_tables()

    def _open_table(self, table: str) -> CsvReader:
        t = CsvReader(table)
        self.tables[table] = t
        return t

    def _save_all_tables(self) -> None:
        for t in self.tables.values():
            t.save()

    def _open_text_files(
        self, filename: str, format: str
    ) -> dict[int, list[tuple[str, str]]]:
        languages = {
            "JPN": 1,
            "Korean": 3,
            "Trad_Chinese": 4,
            "French": 5,
            "German": 6,
            "Spanish": 7,
            "Italian": 8,
            "English": 9,
            "JPN_KANJI": 11,
            "Simp_Chinese": 12,
        }
        result = {}
        for language, language_id in languages.items():
            result[language_id] = self._open_text_file(language, filename, format)
        return result

    def _open_text_file(
        self, language: str, filename: str, format: str
    ) -> list[tuple[str, str]]:
        key = (language, filename, format)
        if key not in self.text_files:
            f = TextFile(self.path, language, filename, format).lines
            self.text_files[key] = f
        return self.text_files[key]

    def _pokemon_stats(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        for i in range(6):
            stat_id = i + 1
            self.pokemon_stats_csv.set_row(
                pokemon_id=pokemon_id,
                stat_id=stat_id,
                base_stat=pokemon.stat(stat_id),
                effort=pokemon.ev_stat(stat_id),
            )

    def _pokemon_types(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        for i in range(2):
            slot = i + 1
            if slot == 2 and pokemon.type_1 == pokemon.type_2:
                continue
            self.pokemon_types_csv.set_row(
                pokemon_id=pokemon_id,
                type_id=pokemon.type(slot),
                slot=slot,
            )

    def _pokemon_species_names(self, pokemon_id: int) -> None:
        lang_names = self._open_text_files("monsname", "swsh")
        for language_id, names in lang_names.items():
            for name in names:
                if name[0] == f"MONSNAME_{pokemon_id:0>3}":
                    self.pokemon_species_names_csv.set_row(
                        pokemon_species_id=pokemon_id,
                        local_language_id=language_id,
                        name=name[1],
                    )
                    continue

    def _pokemon_species_genera(self, pokemon_id: int) -> None:
        lang_genera = self._open_text_files("zkn_type", "swsh")
        for language_id, genera in lang_genera.items():
            for genus in genera:
                if genus[0] == f"ZKN_TYPE_{pokemon_id:0>3}":
                    self.pokemon_species_names_csv.set_row(
                        pokemon_species_id=pokemon_id,
                        local_language_id=language_id,
                        genus=genus[1],
                    )
                    continue

    def _pokemon_species_flavor_text(self, pokemon_id: int) -> None:
        flavor_text_sword = self._open_text_files("zukan_comment_A", "swsh")
        flavor_text_shield = self._open_text_files("zukan_comment_B", "swsh")

    def _pokemon_formes(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        names_en = self._open_text_file("English", "monsname", "swsh")

        if pokemon.has_formes:
            for forme_id in range(1, pokemon.forme_count):
                forme_index = pokemon.forme_index(pokemon_id, forme_id)
                forme = self.personal_table.get_personal_info(forme_index)
                if forme.is_present_in_game:
                    identifier = to_id(names_en[pokemon_id][1])
                    form_name = self.form_names[identifier][forme_id]
                    if form_name is False:
                        continue
                    if form_name:
                        identifier += "-" + form_name

                    forme_pokemon_id = next(
                        (
                            int(i["id"])
                            for i in self.pokemon_csv.entries.values()
                            if i["identifier"] == identifier
                        ),
                        int(max(self.pokemon_csv.entries.keys())[0]) + 1,
                    )
                    self.pokemon_csv.set_row(
                        id=forme_pokemon_id,
                        identifier=identifier,
                        species_id=pokemon_id,
                        height=forme.height // 10,
                        weight=forme.weight,
                        base_experience=forme.base_exp,
                        order_fallback_=10000,
                        is_default=0,
                    )

                    self._pokemon_stats(forme_pokemon_id, forme)
                    self._pokemon_types(forme_pokemon_id, forme)

    def _dump_pokemon(self) -> None:
        names_en = self._open_text_file("English", "monsname", "swsh")

        for pokemon_id in range(1, self.personal_table.last_species_id + 1):
            pokemon = self.personal_table.get_forme_entry(pokemon_id)
            if pokemon.is_present_in_game:
                identifier = to_id(names_en[pokemon_id][1])
                identifier_species = identifier
                if pokemon.has_formes:
                    form_name = self.form_names[identifier][0]
                    if form_name:
                        identifier += "-" + form_name

                self.pokemon_csv.set_row(
                    id=pokemon_id,
                    identifier=identifier,
                    species_id=pokemon_id,
                    height=pokemon.height // 10,
                    weight=pokemon.weight,
                    base_experience=pokemon.base_exp,
                    order_fallback_=10000,
                    is_default=1,
                )

                self.pokemon_species_csv.set_row(
                    id=pokemon_id,
                    identifier=identifier_species,
                    generation_id_fallback_=7 if identifier in self.gen7 else 8,
                    evolves_from_species_id_fallback_="_",
                    evolution_chain_id_fallback_="_",
                    color_id=pokemon.color,
                    shape_id_fallback_="",  # TODO
                    habitat_id_fallback_="",  # it's a fr/lg thing
                    gender_rate=pokemon.gender_ratio,
                    capture_rate=pokemon.catch_rate,
                    base_happiness=pokemon.base_friendship,
                    is_baby=int(pokemon.is_baby),
                    hatch_counter=pokemon.hatch_cycles,
                    has_gender_differences_fallback_=0,  # TODO
                    growth_rate_id=pokemon.exp_growth,
                    forms_switchable_fallback_=0,  # TODO
                    is_legendary_fallback_=1
                    if identifier in self.legendary_list
                    else 0,
                    is_mythical_fallback_=1 if identifier in self.mythical_list else 0,
                    order_fallback_=10000,
                    conquest_order_fallback_="",
                )

                self._pokemon_stats(pokemon_id, pokemon)
                self._pokemon_types(pokemon_id, pokemon)
                self._pokemon_species_names(pokemon_id)
                self._pokemon_species_genera(pokemon_id)
                self._pokemon_species_flavor_text(pokemon_id)

                self._pokemon_formes(pokemon_id, pokemon)

    def _create_evolution_chains(self) -> None:
        max_chain = int(max(self.evolution_chains_csv.entries.keys())[0])
        for key in self.pokemon_species_csv.entries.keys():
            entry = self.pokemon_species_csv.entries[key]
            if entry["evolution_chain_id"] == "_":
                if entry["evolves_from_species_id"] == "_":
                    entry["evolves_from_species_id"] = ""
                    max_chain += 1
                    self.evolution_chains_csv.set_row(id=max_chain)
                    chain = max_chain
                else:
                    chain = int(
                        self.pokemon_species_csv.entries[
                            (int(entry["evolves_from_species_id"]),)
                        ]["evolution_chain_id"]
                    )
                entry["evolution_chain_id"] = str(chain)
                pokemon = self.personal_table.get_personal_info(int(key[0]))
                for evo in pokemon.evos:
                    self.pokemon_species_csv.entries[(evo.species,)][
                        "evolves_from_species_id"
                    ] = str(key[0])

    def _update_pokemon_order(self) -> None:
        ordered_pokemon = sorted(
            [i[0] for i in self.pokemon_csv.entries.keys() if int(i[0]) < 10000],
            key=lambda x: (
                int(self.pokemon_csv.entries[(x,)]["order"]),
                int(self.pokemon_csv.entries[(x,)]["id"]),
            ),
        )
        order = 0
        for pokemon_id in ordered_pokemon:
            order += 1
            self.pokemon_csv.entries[(pokemon_id,)]["order"] = str(order)

            ordered_alternate_formes = sorted(
                [
                    k[0]
                    for k, v in self.pokemon_csv.entries.items()
                    if int(v["species_id"]) == pokemon_id and int(v["is_default"]) == 0
                ],
                key=lambda x: (
                    int(self.pokemon_csv.entries[(x,)]["order"]),
                    int(self.pokemon_csv.entries[(x,)]["id"]),
                ),
            )
            for pokemon_forme_id in ordered_alternate_formes:
                order += 1
                self.pokemon_csv.entries[(pokemon_forme_id,)]["order"] = str(order)

    def _update_pokemon_species_order(self) -> None:
        ordered_pokemon_species = sorted(
            [i[0] for i in self.pokemon_species_csv.entries.keys()],
            key=lambda x: (
                int(self.pokemon_species_csv.entries[(x,)]["order"]),
                int(self.pokemon_species_csv.entries[(x,)]["id"]),
            ),
        )
        order = 0
        for pokemon_id in ordered_pokemon_species:
            order += 1
            self.pokemon_species_csv.entries[(pokemon_id,)]["order"] = str(order)
