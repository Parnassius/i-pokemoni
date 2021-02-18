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
        self.file_format = "swsh"

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
            "zygarde": [
                "50", "10",  # base
                "10-power-construct", "50-power-construct", "complete",  # power construct
            ],
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

        self.personal_table = PersonalTable(self.path, self.file_format)

        self._create_base_records()

        self._dump_abilities()

        self._dump_pokemon()
        self._create_evolution_chains()
        self._update_pokemon_order()
        self._update_pokemon_species_order()

        self._save_all_tables()

    def _open_table(self, table: str) -> CsvReader:
        if table not in self.tables:
            t = CsvReader(table)
            self.tables[table] = t
        return self.tables[table]

    def _save_all_tables(self) -> None:
        for t in self.tables.values():
            t.save()

    def _open_text_files(self, filename: str) -> dict[int, list[tuple[str, str]]]:
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
            result[language_id] = self._open_text_file(language, filename)
        return result

    def _open_text_file(self, language: str, filename: str) -> list[tuple[str, str]]:
        key = (language, filename)
        if key not in self.text_files:
            f = TextFile(self.path, language, filename, self.file_format).lines
            self.text_files[key] = f
        return self.text_files[key]

    def _create_base_records(self) -> None:
        regions_csv = self._open_table("regions")
        region_names_csv = self._open_table("region_names")

        regions_csv.set_row(
            id=8,
            identifier="galar",
        )
        region_names_csv.set_row(  # TODO
            region_id=8,
            local_language_id=9,
            name="Galar",
        )

        generations_csv = self._open_table("generations")
        generation_names_csv = self._open_table("generation_names")

        generations_csv.set_row(
            id=8,
            main_region_id=8,
            identifier="generation-viii",
        )
        generation_names_csv.set_row(  # TODO
            generation_id=8,
            local_language_id=9,
            name="Generation VIII",
        )

        version_groups_csv = self._open_table("version_groups")
        version_group_regions_csv = self._open_table("version_group_regions")

        version_groups_csv.set_row(
            id=20,
            identifier="sword-shield",
            generation_id=8,
            order=20,
        )
        version_group_regions_csv.set_row(
            version_group_id=20,
            region_id=8,
        )

        versions_csv = self._open_table("versions")
        version_names_csv = self._open_table("version_names")

        versions_csv.set_row(
            id=33,
            version_group_id=20,
            identifier="sword",
        )
        version_names_csv.set_row(
            version_id=33,
            local_language_id=9,
            name="Sword",
        )
        versions_csv.set_row(
            id=34,
            version_group_id=20,
            identifier="shield",
        )
        version_names_csv.set_row(
            version_id=34,
            local_language_id=9,
            name="Shield",
        )

        pokedexes_csv = self._open_table("pokedexes")
        pokedex_prose_csv = self._open_table("pokedex_prose")
        pokedex_version_groups_csv = self._open_table("pokedex_version_groups")

        pokedexes_csv.set_row(
            id=27,
            region_id=8,
            identifier="galar",
            is_main_series=1,
        )
        pokedex_prose_csv.set_row(  # TODO
            pokedex_id=27,
            local_language_id=9,
            name="Galar",
        )
        pokedex_version_groups_csv.set_row(
            pokedex_id=27,
            version_group_id=20,
        )
        pokedexes_csv.set_row(
            id=28,
            region_id=8,
            identifier="isle-of-armor",
            is_main_series=1,
        )
        pokedex_prose_csv.set_row(  # TODO
            pokedex_id=28,
            local_language_id=9,
            name="Isle of Armor",
        )
        pokedex_version_groups_csv.set_row(
            pokedex_id=28,
            version_group_id=20,
        )
        pokedexes_csv.set_row(
            id=29,
            region_id=8,
            identifier="crown-tundra",
            is_main_series=1,
        )
        pokedex_prose_csv.set_row(  # TODO
            pokedex_id=29,
            local_language_id=9,
            name="Crown Tundra",
        )
        pokedex_version_groups_csv.set_row(
            pokedex_id=29,
            version_group_id=20,
        )

    def _dump_abilities(self) -> None:
        abilities_csv = self._open_table("abilities")

        abilities_en = self._open_text_file("English", "tokusei")
        for ability in abilities_en:
            ability_id = int(ability[0][-3:])
            if ability_id == 0:
                continue
            identifier = to_id(ability[1])
            if ability_id == 266:
                identifier += "-glastrier"
            elif ability_id == 267:
                identifier += "-spectrier"
            abilities_csv.set_row(
                id=ability_id,
                identifier=identifier,
                generation_id_fallback_=8,
                is_main_series_fallback_=1,
            )

        ability_names_csv = self._open_table("ability_names")

        lang_abilities = self._open_text_files("tokusei")
        for language_id, abilities in lang_abilities.items():
            for ability in abilities:
                ability_id = int(ability[0][-3:])
                if ability_id == 0:
                    continue
                ability_names_csv.set_row(
                    ability_id=ability_id,
                    local_language_id=language_id,
                    name=ability[1],
                )

        ability_flavor_text_csv = self._open_table("ability_flavor_text")

        lang_ability_flavor_text = self._open_text_files("tokuseiinfo")
        for language_id, flavor_text in lang_ability_flavor_text.items():
            for flavor in flavor_text:
                ability_id = int(flavor[0][-3:])
                if ability_id == 0:
                    continue
                ability_flavor_text_csv.set_row(
                    ability_id=ability_id,
                    version_group_id=20,
                    language_id=language_id,
                    flavor_text=flavor[1],
                )

    def _pokemon_stats(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_stats_csv = self._open_table("pokemon_stats")

        for i in range(6):
            stat_id = i + 1
            pokemon_stats_csv.set_row(
                pokemon_id=pokemon_id,
                stat_id=stat_id,
                base_stat=pokemon.stat(stat_id),
                effort=pokemon.ev_stat(stat_id),
            )

    def _pokemon_types(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_types_csv = self._open_table("pokemon_types")

        for i in range(2):
            slot = i + 1
            if slot == 2 and pokemon.type_1 == pokemon.type_2:
                continue
            pokemon_types_csv.set_row(
                pokemon_id=pokemon_id,
                type_id=pokemon.type(slot),
                slot=slot,
            )

    def _pokemon_species_names(self, pokemon_id: int) -> None:
        pokemon_species_names_csv = self._open_table("pokemon_species_names")

        lang_names = self._open_text_files("monsname")
        for language_id, names in lang_names.items():
            for name in names:
                if name[0] == f"MONSNAME_{pokemon_id:0>3}":
                    pokemon_species_names_csv.set_row(
                        pokemon_species_id=pokemon_id,
                        local_language_id=language_id,
                        name=name[1],
                    )
                    continue

    def _pokemon_species_genera(self, pokemon_id: int) -> None:
        pokemon_species_names_csv = self._open_table("pokemon_species_names")

        lang_genera = self._open_text_files("zkn_type")
        for language_id, genera in lang_genera.items():
            for genus in genera:
                if genus[0] == f"ZKN_TYPE_{pokemon_id:0>3}":
                    pokemon_species_names_csv.set_row(
                        pokemon_species_id=pokemon_id,
                        local_language_id=language_id,
                        genus=genus[1],
                    )
                    continue

    def _pokemon_species_flavor_text(self, pokemon_id: int) -> None:
        pokemon_species_flavor_text_csv = self._open_table(
            "pokemon_species_flavor_text"
        )

        files = {
            "A": 33,  # sword
            "B": 34,  # shield
        }
        for version_letter, version_id in files.items():
            lang_flavor_text = self._open_text_files(f"zukan_comment_{version_letter}")
            for language_id, flavor_text in lang_flavor_text.items():
                for flavor in flavor_text:
                    if (
                        flavor[0]
                        == f"ZKN_COMMENT_{version_letter}_{pokemon_id:0>3}_000"
                    ):
                        pokemon_species_flavor_text_csv.set_row(
                            species_id=pokemon_id,
                            version_id=version_id,
                            language_id=language_id,
                            flavor_text=flavor[1],
                        )
                        continue

    def _pokemon_formes(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        names_en = self._open_text_file("English", "monsname")
        pokemon_csv = self._open_table("pokemon")

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
                            for i in pokemon_csv.entries.values()
                            if i["identifier"] == identifier
                        ),
                        int(max(pokemon_csv.entries.keys())[0]) + 1,
                    )

                    # hardcode new zygarde ids
                    if identifier == "zygarde-10-power-construct":
                        forme_pokemon_id = 10118
                    if identifier == "zygarde-50-power-construct":
                        forme_pokemon_id = 10119
                    if identifier == "zygarde-10":
                        forme_pokemon_id = 10179


                    pokemon_csv.set_row(
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

                    self._pokemon_abilities(forme_pokemon_id, forme)

    def _pokemon_dex_numbers(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_dex_numbers_csv = self._open_table("pokemon_dex_numbers")

        dex_numbers = {
            1: pokemon_id,
            27: pokemon.pokedex_index,
            28: pokemon.armordex_index,
            29: pokemon.crowndex_index,
        }
        for pokedex_id, pokedex_number in dex_numbers.items():
            if pokedex_number:
                pokemon_dex_numbers_csv.set_row(
                    species_id=pokemon_id,
                    pokedex_id=pokedex_id,
                    pokedex_number=pokedex_number,
                )

    def _pokemon_abilities(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_abilities_csv = self._open_table("pokemon_abilities")

        abilities = {1: pokemon.ability_1}
        if pokemon.ability_2 not in abilities.values():
            abilities[2] = pokemon.ability_2
        if pokemon.ability_h not in abilities.values():
            abilities[3] = pokemon.ability_h
        for slot, ability in abilities.items():
            pokemon_abilities_csv.set_row(
                pokemon_id=pokemon_id,
                ability_id=ability,
                is_hidden=int(slot == 3),
                slot=slot,
            )

    def _pokemon_egg_groups(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_egg_groups_csv = self._open_table("pokemon_egg_groups")

        egg_groups = {pokemon.egg_group_1, pokemon.egg_group_2}
        for egg_group in egg_groups:
            pokemon_egg_groups_csv.set_row(
                species_id=pokemon_id,
                egg_group_id=egg_group,
            )

    def _dump_pokemon(self) -> None:
        names_en = self._open_text_file("English", "monsname")
        pokemon_csv = self._open_table("pokemon")
        pokemon_species_csv = self._open_table("pokemon_species")

        for pokemon_id in range(1, self.personal_table.last_species_id + 1):
            pokemon = self.personal_table.get_forme_entry(pokemon_id)
            if pokemon.is_present_in_game:
                identifier = to_id(names_en[pokemon_id][1])
                identifier_species = identifier
                if pokemon.has_formes:
                    form_name = self.form_names[identifier][0]
                    if form_name:
                        identifier += "-" + form_name

                pokemon_csv.set_row(
                    id=pokemon_id,
                    identifier=identifier,
                    species_id=pokemon_id,
                    height=pokemon.height // 10,
                    weight=pokemon.weight,
                    base_experience=pokemon.base_exp,
                    order_fallback_=10000,
                    is_default=1,
                )

                pokemon_species_csv.set_row(
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

                self._pokemon_dex_numbers(pokemon_id, pokemon)
                self._pokemon_abilities(pokemon_id, pokemon)
                self._pokemon_egg_groups(pokemon_id, pokemon)

    def _create_evolution_chains(self) -> None:
        pokemon_species_csv = self._open_table("pokemon_species")
        evolution_chains_csv = self._open_table("evolution_chains")

        max_chain = int(max(evolution_chains_csv.entries.keys())[0])
        for key in pokemon_species_csv.entries.keys():
            entry = pokemon_species_csv.entries[key]
            if entry["evolution_chain_id"] == "_":
                if entry["evolves_from_species_id"] == "_":
                    entry["evolves_from_species_id"] = ""
                    max_chain += 1
                    evolution_chains_csv.set_row(id=max_chain)
                    chain = max_chain
                else:
                    chain = int(
                        pokemon_species_csv.entries[
                            (int(entry["evolves_from_species_id"]),)
                        ]["evolution_chain_id"]
                    )
                entry["evolution_chain_id"] = str(chain)
                pokemon = self.personal_table.get_personal_info(int(key[0]))
                for evo in pokemon.evos:
                    pokemon_species_csv.entries[(evo.species,)][
                        "evolves_from_species_id"
                    ] = str(key[0])

    def _update_pokemon_order(self) -> None:
        pokemon_csv = self._open_table("pokemon")

        ordered_pokemon = sorted(
            [i[0] for i in pokemon_csv.entries.keys() if int(i[0]) < 10000],
            key=lambda x: (
                int(pokemon_csv.entries[(x,)]["order"]),
                int(pokemon_csv.entries[(x,)]["id"]),
            ),
        )
        order = 0
        for pokemon_id in ordered_pokemon:
            order += 1
            pokemon_csv.entries[(pokemon_id,)]["order"] = str(order)

            ordered_alternate_formes = sorted(
                [
                    k[0]
                    for k, v in pokemon_csv.entries.items()
                    if int(v["species_id"]) == pokemon_id and int(v["is_default"]) == 0
                ],
                key=lambda x: (
                    # hardcode zygarde-10 order
                    (pokemon_csv.entries[(x,)]["identifier"] != "zygarde-10"),
                    int(pokemon_csv.entries[(x,)]["order"]),
                    int(pokemon_csv.entries[(x,)]["id"]),
                ),
            )
            for pokemon_forme_id in ordered_alternate_formes:
                order += 1
                pokemon_csv.entries[(pokemon_forme_id,)]["order"] = str(order)

    def _update_pokemon_species_order(self) -> None:
        pokemon_species_csv = self._open_table("pokemon_species")

        ordered_pokemon_species = sorted(
            [i[0] for i in pokemon_species_csv.entries.keys()],
            key=lambda x: (
                int(pokemon_species_csv.entries[(x,)]["order"]),
                int(pokemon_species_csv.entries[(x,)]["id"]),
            ),
        )
        order = 0
        for pokemon_id in ordered_pokemon_species:
            order += 1
            pokemon_species_csv.entries[(pokemon_id,)]["order"] = str(order)


# TODO
# pokemon_moves                         # learnsets
# pokemon_items                         # wild held items
# pokemon_forms/pokemon_form_names
# pokemon_form_generations
# pokemon_evolution                     # evolution methods
# pokemon_egg_groups
# moves SON TROPPI GUARDA DOPO
# machines                              # tr?
# locations/location_names
# location_areas/location_area_prose
# items SON TROPPI GUARDA DOPO
# encounters SON TROPPI GUARDA DOPO
