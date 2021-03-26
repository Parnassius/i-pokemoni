from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING, Literal, TypeVar

from base import BaseTable
from csv_reader import CsvReader
from egg_move.egg_move_table import EggMoveTable
from evolution.evolution_set import Evolution
from item.item_table import ItemTable
from learnset.learnset_table import LearnsetTable
from machine.machine_table import MachineTable
from move.move_table import MoveTable
from personal.personal_table import PersonalTable
from text.text_file import TextFile
from utils import read_as_int, to_id

if TYPE_CHECKING:
    from personal.personal_info import PersonalInfo


T = TypeVar("T", bound=BaseTable)


class DumpBase:
    _SECTIONS: list[str]

    _form_names: dict[str, list[str]] = {
        # fmt: off
        "venusaur": ["", "mega"],
        "charizard": ["", "mega-x", "mega-y"],
        "blastoise": ["", "mega"],
        "beedrill": ["", "mega"],
        "pidgeot": ["", "mega"],
        "rattata": ["", "alola"],
        "raticate": ["", "alola", "totem-alola"],
        "pikachu": ["", "original-cap", "hoenn-cap", "sinnoh-cap", "unova-cap", "kalos-cap", "alola-cap", "partner-cap", "starter", "world-cap"],
        "raichu": ["", "alola"],
        "sandshrew": ["", "alola"],
        "sandslash": ["", "alola"],
        "vulpix": ["", "alola"],
        "ninetales": ["", "alola"],
        "diglett": ["", "alola"],
        "dugtrio": ["", "alola"],
        "meowth": ["", "alola", "galar"],
        "persian": ["", "alola"],
        "alakazam": ["", "mega"],
        "geodude": ["", "alola"],
        "graveler": ["", "alola"],
        "golem": ["", "alola"],
        "ponyta": ["", "galar"],
        "rapidash": ["", "galar"],
        "slowpoke": ["", "galar"],
        "slowbro": ["", "mega", "galar"],
        "farfetchd": ["", "galar"],
        "grimer": ["", "alola"],
        "muk": ["", "alola"],
        "gengar": ["", "mega"],
        "exeggutor": ["", "alola"],
        "marowak": ["", "alola", "totem"],
        "weezing": ["", "galar"],
        "kangaskhan": ["", "mega"],
        "mr-mime": ["", "galar"],
        "pinsir": ["", "mega"],
        "gyarados": ["", "mega"],
        "eevee": ["", "starter"],
        "aerodactyl": ["", "mega"],
        "articuno": ["", "galar"],
        "zapdos": ["", "galar"],
        "moltres": ["", "galar"],
        "mewtwo": ["", "mega-x", "mega-y"],
        "ampharos": ["", "mega"],
        "slowking": ["", "galar"],
        "unown": [i + "_" for i in "abcdefghijklmnopqrstuvwxyz"] + ["exclamation_", "question_"],
        "steelix": ["", "mega"],
        "scizor": ["", "mega"],
        "heracross": ["", "mega"],
        "corsola": ["", "galar"],
        "houndoom": ["", "mega"],
        "tyranitar": ["", "mega"],
        "sceptile": ["", "mega"],
        "blaziken": ["", "mega"],
        "swampert": ["", "mega"],
        "zigzagoon": ["", "galar"],
        "linoone": ["", "galar"],
        "gardevoir": ["", "mega"],
        "sableye": ["", "mega"],
        "mawile": ["", "mega"],
        "aggron": ["", "mega"],
        "medicham": ["", "mega"],
        "manectric": ["", "mega"],
        "sharpedo": ["", "mega"],
        "camerupt": ["", "mega"],
        "altaria": ["", "mega"],
        "castform": ["", "sunny", "rainy", "snowy"],
        "banette": ["", "mega"],
        "absol": ["", "mega"],
        "glalie": ["", "mega"],
        "salamence": ["", "mega"],
        "metagross": ["", "mega"],
        "latias": ["", "mega"],
        "latios": ["", "mega"],
        "kyogre": ["", "primal"],
        "groudon": ["", "primal"],
        "rayquaza": ["", "mega"],
        "deoxys": ["normal", "attack", "defense", "speed"],
        "burmy": ["plant_", "sandy_", "trash_"],
        "wormadam": ["plant", "sandy", "trash"],
        "mothim": ["plant_", "sandy_", "trash_"],
        "cherrim": ["overcast_", "sunshine_"],
        "shellos": ["west_", "east_"],
        "gastrodon": ["west_", "east_"],
        "lopunny": ["", "mega"],
        "garchomp": ["", "mega"],
        "lucario": ["", "mega"],
        "abomasnow": ["", "mega"],
        "gallade": ["", "mega"],
        "rotom": ["", "heat", "wash", "frost", "fan", "mow"],
        "giratina": ["altered", "origin"],
        "shaymin": ["land", "sky"],
        "arceus": ["normal_", "fighting_", "flying_", "poison_", "ground_", "rock_", "bug_", "ghost_", "steel_", "fire_", "water_", "grass_", "electric_", "psychic_", "ice_", "dragon_", "dark_", "fairy_"],
        "audino": ["", "mega"],
        "basculin": ["red-striped", "blue-striped"],
        "darumaka": ["", "galar"],
        "darmanitan": ["standard", "zen", "galar-standard", "galar-zen"],
        "yamask": ["", "galar"],
        "deerling": ["spring_", "summer_", "autumn_", "winter_"],
        "sawsbuck": ["spring_", "summer_", "autumn_", "winter_"],
        "stunfisk": ["", "galar"],
        "tornadus": ["incarnate", "therian"],
        "thundurus": ["incarnate", "therian"],
        "landorus": ["incarnate", "therian"],
        "kyurem": ["", "white", "black"],
        "keldeo": ["ordinary", "resolute"],
        "meloetta": ["aria", "pirouette"],
        "genesect": ["", "douse_", "shock_", "burn_", "chill_"],  # ?
        "greninja": ["", "battle-bond", "ash"],
        "scatterbug": ["icy-snow_", "polar_", "tundra_", "continental_", "garden_", "elegant_", "meadow_", "modern_", "marine_", "archipelago_", "high-plains_", "sandstorm_", "river_", "monsoon_", "savanna_", "sun_", "ocean_", "jungle_", "fancy_", "poke-ball_"],
        "spewpa": ["icy-snow_", "polar_", "tundra_", "continental_", "garden_", "elegant_", "meadow_", "modern_", "marine_", "archipelago_", "high-plains_", "sandstorm_", "river_", "monsoon_", "savanna_", "sun_", "ocean_", "jungle_", "fancy_", "poke-ball_"],
        "vivillon": ["icy-snow_", "polar_", "tundra_", "continental_", "garden_", "elegant_", "meadow_", "modern_", "marine_", "archipelago_", "high-plains_", "sandstorm_", "river_", "monsoon_", "savanna_", "sun_", "ocean_", "jungle_", "fancy_", "poke-ball_"],
        "flabebe": ["red_", "yellow_", "orange_", "blue_", "white_"],
        "floette": ["red_", "yellow_", "orange_", "blue_", "white_", "eternal"],
        "florges": ["red_", "yellow_", "orange_", "blue_", "white_"],
        "furfrou": ["natural_", "heart_", "star_", "diamond_", "debutante_", "matron_", "dandy_", "la-reine_", "kabuki_", "pharaoh_"],
        "meowstic": ["male", "female"],
        "aegislash": ["shield", "blade"],
        "pumpkaboo": ["average", "small", "large", "super"],
        "gourgeist": ["average", "small", "large", "super"],
        "xerneas": ["neutral_", "active_"],  # active is the main one
        "zygarde": [
            "50", "10",  # base
            "10-power-construct", "50-power-construct", "complete",  # power construct
        ],
        "diancie": ["", "mega"],
        "hoopa": ["", "unbound"],
        "gumshoos": ["", "totem"],
        "vikavolt": ["", "totem"],
        "oricorio": ["baile", "pom-pom", "pau", "sensu"],
        "ribombee": ["", "totem"],
        "rockruff": ["", "own-tempo"],
        "lycanroc": ["midday", "midnight", "dusk"],
        "wishiwashi": ["solo", "school"],
        "araquanid": ["", "totem"],
        "lurantis": ["", "totem"],
        "salazzle": ["", "totem"],
        "silvally": ["normal_", "fighting_", "flying_", "poison_", "ground_", "rock_", "bug_", "ghost_", "steel_", "fire_", "water_", "grass_", "electric_", "psychic_", "ice_", "dragon_", "dark_", "fairy_"],
        "minior": ["red-meteor", "orange-meteor", "yellow-meteor", "green-meteor", "blue-meteor", "indigo-meteor", "violet-meteor", "red", "orange", "yellow", "green", "blue", "indigo", "violet"],
        "togedemaru": ["", "totem"],
        "mimikyu": ["disguised", "busted", "totem-disguised", "totem-busted"],
        "kommo-o": ["", "totem"],
        "necrozma": ["", "dusk", "dawn", "ultra"],
        "magearna": ["", "original"],
        "cramorant": ["", "gulping", "gorging"],
        "toxtricity": ["amped", "low-key"],
        "sinistea": ["phony_", "antique_"],
        "polteageist": ["phony_", "antique_"],
        "alcremie": ["vanilla-cream_", "ruby-cream_", "matcha-cream_", "mint-cream_", "lemon-cream_", "salted-cream_", "ruby-swirl_", "caramel-swirl_", "rainbow-swirl_"],
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
    _legendary_list = [
        # fmt: off
        "zacian", "zamazenta", "eternatus",
        "kubfu", "urshifu",
        "regieleki", "regidrago", "glastrier", "spectrier", "calyrex",
    ]
    _mythical_list = ["zarude"]
    _item_suffixes = {
        780: "jacket",  # contest-costume
        817: "held",  # normalium-z
        818: "held",  # firium-z
        819: "held",  # waterium-z
        820: "held",  # electrium-z
        821: "held",  # grassium-z
        822: "held",  # icium-z
        823: "held",  # fightinium-z
        824: "held",  # poisonium-z
        825: "held",  # groundium-z
        826: "held",  # flyinium-z
        827: "held",  # psychium-z
        828: "held",  # buginium-z
        829: "held",  # rockium-z
        830: "held",  # ghostium-z
        831: "held",  # dragonium-z
        832: "held",  # darkinium-z
        833: "held",  # steelium-z
        834: "held",  # fairium-z
        835: "held",  # pikanium-z
        839: "held",  # decidium-z
        840: "held",  # incinium-z
        841: "held",  # primarium-z
        842: "held",  # tapunium-z
        843: "held",  # marshadium-z
        844: "held",  # aloraichium-z
        845: "held",  # snorlium-z
        846: "held",  # eevium-z
        847: "held",  # mewnium-z
        877: "held",  # pikashunium-z
        919: "green",  # bike
        920: "galactic-warehouse",  # storage-key
        921: "goldenrod",  # basement-key
        922: "red",  # xtransceiver
        923: "yellow",  # xtransceiver
        924: "merge",  # dna-splicers
        925: "split",  # dna-splicers
        926: "red",  # dropped-item
        927: "yellow",  # dropped-item
        928: "green",  # holo-caster
        929: "yellow",  # bike
        930: "red",  # holo-caster
        931: "new-mauville",  # basement-key
        932: "sea-mauville",  # storage-key
        933: "hoenn",  # ss-ticket
        934: "dress",  # contest-costume
        935: "2",  # meteorite
        936: "3",  # meteorite
        937: "4",  # meteorite
        938: "bag",  # normalium-z
        939: "bag",  # firium-z
        940: "bag",  # waterium-z
        941: "bag",  # electrium-z
        942: "bag",  # grassium-z
        943: "bag",  # icium-z
        944: "bag",  # fightinium-z
        945: "bag",  # poisonium-z
        946: "bag",  # groundium-z
        947: "bag",  # flyinium-z
        948: "bag",  # psychium-z
        949: "bag",  # buginium-z
        950: "bag",  # rockium-z
        951: "bag",  # ghostium-z
        952: "bag",  # dragonium-z
        953: "bag",  # darkinium-z
        954: "bag",  # steelium-z
        955: "bag",  # fairium-z
        956: "bag",  # pikanium-z
        957: "bag",  # decidium-z
        958: "bag",  # incinium-z
        959: "bag",  # primarium-z
        960: "bag",  # tapunium-z
        961: "bag",  # marshadium-z
        962: "bag",  # aloraichium-z
        963: "bag",  # snorlium-z
        964: "bag",  # eevium-z
        965: "bag",  # mewnium-z
        966: "bag",  # pikashunium-z
        967: "held",  # solganium-z
        968: "held",  # lunalium-z
        969: "held",  # ultranecrozium-z
        970: "held",  # mimikium-z
        971: "held",  # lycanium-z
        972: "held",  # kommonium-z
        973: "bag",  # solganium-z
        974: "bag",  # lunalium-z
        975: "bag",  # ultranecrozium-z
        976: "bag",  # mimikium-z
        977: "bag",  # lycanium-z
        978: "bag",  # kommonium-z
        989: "merge",  # n-solarizer
        990: "merge",  # n-lunarizer
        991: "split",  # n-solarizer
        992: "split",  # n-lunarizer
        1021: "letsgo",  # ss-ticket
        1023: "letsgo",  # card-key
        1020: "letsgo",  # secret-key
        1022: "letsgo",  # parcel
        1033: "pikachu",  # leaf-letter
        1034: "eevee",  # leaf-letter
        1324: "water-mode",  # rotom-bike
        1636: "sparkling-white",  # rotom-bike
        1637: "glistening-black",  # rotom-bike
        1641: "merge",  # reins-of-unity
        1642: "split",  # reins-of-unity
        # 1658: "",  # reins-of-unity
        1142: "galar",  # fishing-rod
    }
    _identifier_overrides = {
        "upgrade": "up-grade",
        "leek": "stick",
        "health-feather": "health-wing",
        "muscle-feather": "muscle-wing",
        "resist-feather": "resist-wing",
        "genius-feather": "genius-wing",
        "clever-feather": "clever-wing",
        "swift-feather": "swift-wing",
        "pretty-feather": "pretty-wing",
        "adventure-guide": "adventure-rules",
        "ilima-normalium-z": "ilimas-normalium-z",
        "legendary-clue?": "legendary-clue-question",
        "vise-grip": "vice-grip",
    }
    _identifier_overrides_game_index: dict[int, str] = {}
    _languages = {
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

    _new_items: set[int] = set()
    _changed_items: dict[int, int] = {}

    _new_item_categories: dict[int, tuple[str, int, dict[int, str]]] = {}

    _new_evolution_methods: dict[int, tuple[str, dict[int, str]]] = {}

    _new_move_meta_ailments: dict[int, tuple[str, dict[int, str]]] = {}

    _region_id: int
    _region_identifier: str
    _region_names: dict[int, str]

    _generation_id: int
    _generation_identifier: str
    _generation_main_region: int
    _generation_names: dict[int, str]

    _version_group_id: int
    _version_group_identifier: str
    _version_group_order: int

    _version_ids: list[int]
    _version_identifiers: list[str]
    _version_names: list[dict[int, str]]

    _pokedex_ids: list[int]
    _pokedex_identifiers: list[str]
    _pokedex_names: list[dict[int, tuple[str, str]]]

    _single_flavor_text: bool = False

    _type_tutors: list[int] = []
    _special_tutors: list[list[int]] = []
    _hardcode_tutors: dict[int, int] = {}

    def __init__(self, sections: list) -> None:
        self._path: str
        self._format: str

        self._sections = sections

        self._csvs: dict[str, CsvReader] = {}
        self._tables: dict[type[BaseTable], BaseTable] = {}
        self._text_files: dict[tuple[str, ...], list[tuple[str, str]]] = {}

        self._create_base_records()

        if "moves" in self._sections:
            self._dump_moves()

        if "abilities" in self._sections:
            self._dump_abilities()

        if "items" in self._sections:
            self._dump_items()

        if "machines" in self._sections:
            self._dump_machines()

        if "pokemon" in self._sections or "learnsets" in self._sections:
            self._dump_pokemon()

        self._save_all_csvs()

    def _open_csv(self, table: str) -> CsvReader:
        if table not in self._csvs:
            t = CsvReader(table)
            self._csvs[table] = t
        return self._csvs[table]

    def _save_all_csvs(self) -> None:
        for t in self._csvs.values():
            t.save()

    def _open_table(self, cls_: type[T]) -> T:
        if cls_ not in self._tables:
            t = cls_(self._path, self._format)
            self._tables[cls_] = t
        return self._tables[cls_]  # type: ignore[return-value]

    def _open_text_files(self, filename: str) -> dict[int, list[tuple[str, str]]]:
        result = {}
        for language, language_id in self._languages.items():
            result[language_id] = self._open_text_file(language, filename)
        return result

    def _open_text_file(self, language: str, filename: str) -> list[tuple[str, str]]:
        key = (language, filename)
        if key not in self._text_files:
            f = TextFile(self._path, language, filename, self._format).lines
            self._text_files[key] = f
        return self._text_files[key]

    def _get_item_id_from_game_index(self, game_index: int) -> int | None:
        item_game_indices_csv = self._open_csv("item_game_indices")
        return next(
            (
                int(i["item_id"])
                for i in item_game_indices_csv.entries.values()
                if int(i["generation_id"]) == self._generation_id
                and int(i["game_index"]) == game_index
            ),
            None,
        )

    def _create_base_records(self) -> None:
        regions_csv = self._open_csv("regions")
        region_names_csv = self._open_csv("region_names")

        regions_csv.set_row(
            id=self._region_id,
            identifier=self._region_identifier,
        )
        for language_id, region_name in self._region_names.items():
            region_names_csv.set_row(
                region_id=self._region_id,
                local_language_id=language_id,
                name=region_name,
            )

        generations_csv = self._open_csv("generations")
        generation_names_csv = self._open_csv("generation_names")

        generations_csv.set_row(
            id=self._generation_id,
            main_region_id=self._generation_main_region,
            identifier=self._generation_identifier,
        )
        for language_id, generation_name in self._generation_names.items():
            generation_names_csv.set_row(
                generation_id=self._generation_id,
                local_language_id=language_id,
                name=generation_name,
            )

        version_groups_csv = self._open_csv("version_groups")
        version_group_regions_csv = self._open_csv("version_group_regions")

        version_groups_csv.set_row(
            id=self._version_group_id,
            identifier=self._version_group_identifier,
            generation_id=self._generation_id,
            order=self._version_group_order,
        )
        version_group_regions_csv.set_row(
            version_group_id=self._version_group_id,
            region_id=self._region_id,
        )

        versions_csv = self._open_csv("versions")
        version_names_csv = self._open_csv("version_names")

        for version_id, version_identifier, version_names in zip(
            self._version_ids, self._version_identifiers, self._version_names
        ):
            versions_csv.set_row(
                id=version_id,
                version_group_id=self._version_group_id,
                identifier=version_identifier,
            )
            for language_id, version_name in version_names.items():
                version_names_csv.set_row(
                    version_id=version_id,
                    local_language_id=language_id,
                    name=version_name,
                )

        pokedexes_csv = self._open_csv("pokedexes")
        pokedex_prose_csv = self._open_csv("pokedex_prose")
        pokedex_version_groups_csv = self._open_csv("pokedex_version_groups")

        for pokedex_id, pokedex_identifier, pokedex_names in zip(
            self._pokedex_ids, self._pokedex_identifiers, self._pokedex_names
        ):
            pokedexes_csv.set_row(
                id=pokedex_id,
                region_id=self._region_id,
                identifier=pokedex_identifier,
                is_main_series=1,
            )
            pokedex_version_groups_csv.set_row(
                pokedex_id=pokedex_id,
                version_group_id=self._version_group_id,
            )
            for language_id, pokedex_name in pokedex_names.items():
                pokedex_prose_csv.set_row(
                    pokedex_id=pokedex_id,
                    local_language_id=language_id,
                    name=pokedex_name[0],
                    description_fallback_=pokedex_name[1],
                )

        if self._new_item_categories:
            item_categories_csv = self._open_csv("item_categories")
            item_category_prose_csv = self._open_csv("item_category_prose")

            for category_id, category_data in self._new_item_categories.items():
                item_categories_csv.set_row(
                    id=category_id,
                    pocket_id=category_data[1],
                    identifier=category_data[0],
                )
                for language_id, category_name in category_data[2].items():
                    item_category_prose_csv.set_row(
                        item_category_id=category_id,
                        local_language_id=language_id,
                        name=category_name,
                    )

        if self._new_evolution_methods:
            evolution_triggers_csv = self._open_csv("evolution_triggers")
            evolution_trigger_prose_csv = self._open_csv("evolution_trigger_prose")

            for trigger_id, trigger_data in self._new_evolution_methods.items():
                evolution_triggers_csv.set_row(
                    id=trigger_id,
                    identifier=trigger_data[0],
                )
                for language_id, trigger_name in trigger_data[1].items():
                    evolution_trigger_prose_csv.set_row(
                        evolution_trigger_id=trigger_id,
                        local_language_id=language_id,
                        name=trigger_name,
                    )

        if self._new_move_meta_ailments:
            move_meta_ailments_csv = self._open_csv("move_meta_ailments")
            move_meta_ailment_names_csv = self._open_csv("move_meta_ailment_names")

            for ailment_id, ailment_data in self._new_move_meta_ailments.items():
                move_meta_ailments_csv.set_row(
                    id=ailment_id,
                    identifier=ailment_data[0],
                )
                for language_id, ailment_name in ailment_data[1].items():
                    move_meta_ailment_names_csv.set_row(
                        move_meta_ailment_id=ailment_id,
                        local_language_id=language_id,
                        name=ailment_name,
                    )

    def _move_names(self) -> None:
        move_names_csv = self._open_csv("move_names")

        lang_moves = self._open_text_files("wazaname")
        for language_id, moves in lang_moves.items():
            for move in moves:
                move_id = int(move[0][move[0].find("_") + 1 :])
                if move_id == 0:
                    continue

                move_names_csv.set_row(
                    move_id=move_id,
                    local_language_id=language_id,
                    name=move[1],
                )

        move_flavor_text_csv = self._open_csv("move_flavor_text")

        lang_move_flavor_text = self._open_text_files("wazainfo")
        for language_id, flavor_text in lang_move_flavor_text.items():
            for flavor in flavor_text:
                move_id = int(flavor[0][flavor[0].find("_") + 1 :])
                if move_id == 0:
                    continue

                move_flavor_text_csv.set_row(
                    move_id=move_id,
                    version_group_id=self._version_group_id,
                    language_id=language_id,
                    flavor_text=flavor[1],
                )

    def _dump_machines(self) -> None:
        machine_table = self._open_table(MachineTable)

        machines_csv = self._open_csv("machines")
        items_csv = self._open_csv("items")

        for machine in machine_table._table:
            item_id = next(
                k[0]
                for k, v in items_csv.entries.items()
                if v["identifier"] == machine.machine_name
            )

            machines_csv.set_row(
                machine_number=machine.machine_number,
                version_group_id=self._version_group_id,
                item_id=item_id,
                move_id=machine.move_id,
            )

    def _dump_moves(self) -> None:
        move_table = self._open_table(MoveTable)

        moves_csv = self._open_csv("moves")
        move_changelog_csv = self._open_csv("move_changelog")
        move_meta_csv = self._open_csv("move_meta")
        move_flag_map_csv = self._open_csv("move_flag_map")
        move_meta_stat_changes_csv = self._open_csv("move_meta_stat_changes")
        move_effects_csv = self._open_csv("move_effects")
        move_effect_prose_csv = self._open_csv("move_effect_prose")

        changelog_columns = {
            "type_id",
            "power",
            "pp",
            "accuracy",
            "priority",
            "target_id",
            "effect_id",
            "effect_chance",
        }

        moves_en = self._open_text_file("English", "wazaname")
        for move in moves_en:
            move_id = int(move[0][move[0].find("_") + 1 :])
            if move_id == 0:
                continue
            identifier = to_id(move[1])

            if identifier in self._identifier_overrides:
                identifier = self._identifier_overrides[identifier]

            move_info = move_table.get_info_from_index(move_id)

            if 622 <= move_id <= 657:  # z-moves
                identifier += (
                    "--" + {2: "physical", 3: "special"}[move_info.damage_class_id]
                )

            if (move_info.effect_id,) not in move_effects_csv.entries.keys():
                move_effects_csv.set_row(
                    id=move_info.effect_id,
                )
                move_effect_prose_csv.set_row(
                    move_effect_id=move_info.effect_id,
                    local_language_id=9,
                    short_effect=f"XXX new effect for {identifier}",
                    effect=f"XXX new effect for {identifier}",
                )

            move_row = moves_csv.entries.get((move_id,))
            if move_row:
                rows = (
                    i
                    for i in move_changelog_csv.entries.keys()
                    if i[0] == move_id and int(i[1]) >= self._version_group_id
                )
                if not any(rows):
                    changed_columns = {}
                    for col in changelog_columns:
                        if str(move_row[col]) != str(getattr(move_info, col)):
                            changed_columns[col] = move_row[col]
                    if changed_columns:
                        move_changelog_csv.set_row(
                            move_id=move_id,
                            changed_in_version_group_id=self._version_group_id,
                            **changed_columns,
                        )

            moves_csv.set_row(
                id=move_id,
                identifier=identifier,
                generation_id_fallback_=self._generation_id,
                type_id=move_info.type_id,
                power=move_info.power,
                pp=move_info.pp,
                accuracy=move_info.accuracy,
                priority=move_info.priority,
                target_id=move_info.target_id,
                damage_class_id=move_info.damage_class_id,
                effect_id=move_info.effect_id,
                effect_chance=move_info.effect_chance,
                # contest_type_id
                # contest_effect_id
                # super_contest_effect_id
            )

            move_meta_csv.set_row(
                move_id=move_id,
                meta_category_id=move_info.meta_category_id,
                meta_ailment_id=move_info.meta_ailment_id,
                min_hits=move_info.hit_min or "",
                max_hits=move_info.hit_max or "",
                min_turns=move_info.turn_min or "",
                max_turns=move_info.turn_max or "",
                drain=move_info.recoil,
                healing=move_info.healing,
                crit_rate=move_info.crit_stage,
                ailment_chance=move_info.inflict_percent,
                flinch_chance=move_info.flinch,
                stat_chance=move_info.stat_chance,
            )

            chances = [
                move_info.inflict_percent,
                move_info.flinch,
                move_info.stat_1_percent,
                move_info.stat_2_percent,
                move_info.stat_3_percent,
            ]
            if len(set(i for i in chances if i)) > 1:
                print(
                    f"{identifier:20}",
                    move_info.inflict_percent,
                    move_info.flinch,
                    move_info.stat_1_percent,
                    move_info.stat_2_percent,
                    move_info.stat_3_percent,
                )

            for flag_id in move_info.flags(identifier):
                move_flag_map_csv.set_row(
                    move_id=move_id,
                    move_flag_id=flag_id,
                )
            for entry in list(move_flag_map_csv.entries):
                if entry[0] == move_id and entry[1] not in move_info.flags(identifier):
                    del move_flag_map_csv.entries[entry]

            for i in range(3):
                stat_ids, change = move_info.stat_change(i)
                if change:
                    for stat_id in stat_ids:
                        move_meta_stat_changes_csv.set_row(
                            move_id=move_id,
                            stat_id=stat_id,
                            change=change,
                        )
            for entry in list(move_meta_stat_changes_csv.entries):
                if entry[0] == move_id and entry[1] not in move_info.stat_changes:
                    del move_meta_stat_changes_csv.entries[entry]

        self._move_names()

    def _dump_abilities(self) -> None:
        abilities_csv = self._open_csv("abilities")

        abilities_en = self._open_text_file("English", "tokusei")
        for ability in abilities_en:
            ability_id = int(ability[0][-3:])
            if ability_id == 0:
                continue
            identifier = to_id(ability[1])

            # hardcode as-one identifiers
            if ability_id == 266:
                identifier += "-glastrier"
            elif ability_id == 267:
                identifier += "-spectrier"

            abilities_csv.set_row(
                id=ability_id,
                identifier=identifier,
                generation_id_fallback_=self._generation_id,
                is_main_series_fallback_=1,
            )

        ability_names_csv = self._open_csv("ability_names")

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

        ability_flavor_text_csv = self._open_csv("ability_flavor_text")

        lang_ability_flavor_text = self._open_text_files("tokuseiinfo")
        for language_id, flavor_text in lang_ability_flavor_text.items():
            for flavor in flavor_text:
                ability_id = int(flavor[0][-3:])
                if ability_id == 0:
                    continue
                ability_flavor_text_csv.set_row(
                    ability_id=ability_id,
                    version_group_id=self._version_group_id,
                    language_id=language_id,
                    flavor_text=flavor[1],
                )

    def _item_names(self) -> None:
        item_names_csv = self._open_csv("item_names")

        lang_items = self._open_text_files("itemname")
        for language_id, items in lang_items.items():
            for item in items:
                game_index = int(item[0][item[0].find("_") + 1 :])
                if game_index == 0:
                    continue

                item_id = self._get_item_id_from_game_index(game_index)

                if item_id:
                    item_names_csv.set_row(
                        item_id=item_id,
                        local_language_id=language_id,
                        name=item[1],
                    )

        item_flavor_text_csv = self._open_csv("item_flavor_text")

        lang_item_flavor_text = self._open_text_files("iteminfo")
        for language_id, flavor_text in lang_item_flavor_text.items():
            for flavor in flavor_text:
                game_index = int(flavor[0][flavor[0].find("_") + 1 :])
                if game_index == 0:
                    continue

                item_id = self._get_item_id_from_game_index(game_index)

                if item_id:
                    item_flavor_text_csv.set_row(
                        item_id=item_id,
                        version_group_id=self._version_group_id,
                        language_id=language_id,
                        flavor_text=flavor[1],
                    )

    def _dump_items(self) -> None:
        """
        itemname/itemname_acc (Protein)
        itemname_classified/itemname_acc_classified (bottle of Protein)
        itemname_plural (Proteins)
        itemname_plural_classified (bottles of Protein)

        differences in swsh between itemname / itemname_acc:
        German:
            ITEMNAME_110 Ovaler Stein / Ovalen Stein
            ITEMNAME_244 Spitzer Schnabel / Spitzen Schnabel
            ITEMNAME_260 Roter Schal / Roten Schal
            ITEMNAME_261 Blauer Schal / Blauen Schal
            ITEMNAME_263 Grüner Schal / Grünen Schal
            ITEMNAME_264 Gelber Schal / Gelben Schal
            ITEMNAME_534 Roter Edelstein / Roten Edelstein
            ITEMNAME_535 Blauer Edelstein / Blauen Edelstein
            ITEMNAME_584 Alter Heller / Alten Heller
            ITEMNAME_585 Alter Taler / Alten Taler
            ITEMNAME_586 Alter Dukat / Alten Dukaten
            ITEMNAME_588 Alter Reif / Alten Reif
            ITEMNAME_635 Achromat / Achromaten
            ITEMNAME_697 Kurioser Stein / Kuriosen Stein
            ITEMNAME_698 Normaler Stein / Normalen Stein
            ITEMNAME_853 Roter Nektar / Roten Nektar
            ITEMNAME_854 Gelber Nektar / Gelben Nektar
            ITEMNAME_856 Purpurner Nektar / Purpurnen Nektar
            ITEMNAME_1092 Dicker Lauch / Dicken Lauch
            ITEMNAME_1103 Rostiges Schwert / Rostige Schwert
            ITEMNAME_1104 Rostiger Schild / Rostigen Schild
            ITEMNAME_1116 Süßer Apfel / Süßen Apfel
            ITEMNAME_1117 Saurer Apfel / Sauren Apfel
            ITEMNAME_1269 Vergilbter Brief / Vergilbten Brief
        Italian:
            ITEMNAME_467: Chiave segreta / Chiave Segreta
        Simp_Chinese:
            ITEMNAME_045: ＨＰ增强剂 / HP增强剂
            ITEMNAME_728: ＧＯＧＯ护目镜 / GOGO护目镜

        differences in swsh between itemname_classified / itemname_acc_classified:
        German:
            ITEMNAME_110 Ovaler Stein / Ovalen Stein
            ITEMNAME_244 Spitzer Schnabel / Spitzen Schnabel
            ITEMNAME_260 Roter Schal / Roten Schal
            ITEMNAME_261 Blauer Schal / Blauen Schal
            ITEMNAME_263 Grüner Schal / Grünen Schal
            ITEMNAME_264 Gelber Schal / Gelben Schal
            ITEMNAME_534 Roter Edelstein / Roten Edelstein
            ITEMNAME_535 Blauer Edelstein / Blauen Edelstein
            ITEMNAME_584 Alter Heller / Alten Heller
            ITEMNAME_585 Alter Taler / Alten Taler
            ITEMNAME_586 Alter Dukat / Alten Dukaten
            ITEMNAME_588 Alter Reif / Alten Reif
            ITEMNAME_635 Achromat / Achromaten
            ITEMNAME_697 Kurioser Stein / Kuriosen Stein
            ITEMNAME_698 Normaler Stein / Normalen Stein
            ITEMNAME_1104 Rostiger Schild / Rostigen Schild
            ITEMNAME_1116 Süßer Apfel / Süßen Apfel
            ITEMNAME_1117 Saurer Apfel / Sauren Apfel
            ITEMNAME_1269 Vergilbter Brief / Vergilbten Brief
        JPN_KANJI:
            ITEMNAME_1591: キヅナのタヅナ / キズナのタヅナ
            ITEMNAME_1607: キヅナのタヅナ / キズナのタヅナ
        """
        item_table = self._open_table(ItemTable)

        items_csv = self._open_csv("items")
        item_game_indices_csv = self._open_csv("item_game_indices")

        items_en = self._open_text_file("English", "itemname")
        for item in items_en:
            game_index = int(item[0][item[0].find("_") + 1 :])
            if game_index == 0:
                continue
            identifier = to_id(item[1])

            if identifier == "???":
                continue

            if identifier in self._identifier_overrides:
                identifier = self._identifier_overrides[identifier]

            if game_index in self._identifier_overrides_game_index:
                identifier = self._identifier_overrides_game_index[game_index]

            items = {
                int(i["item_id"])
                for i in item_game_indices_csv.entries.values()
                if int(i["game_index"]) == game_index
            }
            item_id: set[int] | int
            item_id = {
                int(i["item_id"])
                for i in item_game_indices_csv.entries.values()
                if int(i["generation_id"]) == self._generation_id
                and int(i["game_index"]) == game_index
            }
            if not item_id and game_index in self._changed_items:
                item_id = self._changed_items[game_index]
            if not item_id:
                item_id = {
                    int(i["id"])
                    for i in items_csv.entries.values()
                    if int(i["id"]) in items and i["identifier"] == identifier
                }
            if not item_id:
                item_id_and_identifier = {
                    (int(i["id"]), i["identifier"])
                    for i in items_csv.entries.values()
                    if int(i["id"]) in items
                    and i["identifier"].startswith(f"{identifier}--")
                }
                if len(item_id_and_identifier) == 1:
                    item_id, identifier = list(item_id_and_identifier)[0]

            # new items
            if not item_id or game_index in self._new_items:
                item_id = int(max(items_csv.entries.keys())[0]) + 1

            if isinstance(item_id, set) and len(item_id) != 1:
                print(
                    game_index,
                    identifier,
                    {
                        k[0]: v["identifier"]
                        for k, v in items_csv.entries.items()
                        if int(v["id"]) in items
                    },
                )

            if isinstance(item_id, set):
                item_id = list(item_id)[0]

            if item_id in self._item_suffixes:
                identifier = (
                    identifier.split("--")[0] + "--" + self._item_suffixes[item_id]
                )

            item_info = item_table.get_info_from_index(game_index)

            category_id = 0
            row = items_csv.entries.get((item_id,))
            if row is None or row["category_id"] == "":
                category_id = item_info.category_id(identifier)

            items_csv.set_row(
                id=item_id,
                identifier=identifier,
                category_id_fallback_=category_id or "",
                cost=item_info.buy_price or False,
                cost_fallback_=item_info.buy_price,
                fling_power=item_info.fling_power or False,
                fling_power_fallback_=item_info.fling_power or "",
                fling_effect_id=item_info.fling_effect_id or False,
                fling_effect_id_fallback_=item_info.fling_effect_id or "",
            )

            item_game_indices_csv.set_row(
                item_id=item_id,
                generation_id=self._generation_id,
                game_index=game_index,
            )

        self._item_names()

    def _pokemon_stats(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_stats_csv = self._open_csv("pokemon_stats")

        for i in range(6):
            stat_id = i + 1
            pokemon_stats_csv.set_row(
                pokemon_id=pokemon_id,
                stat_id=stat_id,
                base_stat=pokemon.stat(stat_id),
                effort=pokemon.ev_stat(stat_id),
            )

    def _pokemon_types(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_types_csv = self._open_csv("pokemon_types")

        for i in range(2):
            if i == 1 and pokemon.types[0] == pokemon.types[1]:
                continue
            pokemon_types_csv.set_row(
                pokemon_id=pokemon_id,
                type_id=pokemon.types[i],
                slot=i + 1,
            )

    def _pokemon_species_names(self, pokemon_id: int) -> None:
        pokemon_species_names_csv = self._open_csv("pokemon_species_names")

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
        pokemon_species_names_csv = self._open_csv("pokemon_species_names")

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
        pokemon_species_flavor_text_csv = self._open_csv("pokemon_species_flavor_text")

        if self._single_flavor_text:
            files = {"A": self._version_ids}
        else:
            files = {k: [v] for k, v in zip("AB", self._version_ids)}
        for version_letter, version_ids in files.items():
            lang_flavor_text = self._open_text_files(f"zukan_comment_{version_letter}")
            for language_id, flavor_text in lang_flavor_text.items():
                for flavor in flavor_text:
                    if (
                        flavor[0]
                        == f"ZKN_COMMENT_{version_letter}_{pokemon_id:0>3}_000"
                    ):
                        for version_id in version_ids:
                            pokemon_species_flavor_text_csv.set_row(
                                species_id=pokemon_id,
                                version_id=version_id,
                                language_id=language_id,
                                flavor_text=flavor[1],
                            )
                        continue

    def _pokemon_form_names(
        self, pokemon_id: int, forme_id: int, pokemon_form_id: int
    ) -> None:

        if pokemon_id in (
            201,  # unown forms are all called "One Form"
            493,  # arceus doesn't have form names
            649,  # genesect doesn't have form names
        ):
            return

        pokemon_form_names_csv = self._open_csv("pokemon_form_names")

        lang_names = self._open_text_files("zkn_form")
        for language_id, names in lang_names.items():
            for name in names:
                if name[0] == f"ZKN_FORM_{pokemon_id:0>3}_{forme_id:0>3}":
                    pokemon_form_names_csv.set_row(
                        pokemon_form_id=pokemon_form_id,
                        local_language_id=language_id,
                        form_name=""
                        if pokemon_form_id == 10357  # eternamax
                        else name[1].strip(),
                        # pokemon_name  # TODO
                    )
                    continue

    def _pokemon_formes(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        personal_table = self._open_table(PersonalTable)

        pokemon_forms_csv = self._open_csv("pokemon_forms")
        pokemon_csv = self._open_csv("pokemon")
        pokemon_form_generations_csv = self._open_csv("pokemon_form_generations")

        default_pokemon_list = []

        names_en = self._open_text_file("English", "monsname")
        forms_en = self._open_text_file("English", "zkn_form")
        for forme_id in range(pokemon.forme_count):
            forme_index = pokemon.forme_index(pokemon_id, forme_id)
            forme = personal_table.get_info_from_index(forme_index)
            if forme.is_present_in_game:
                identifier = to_id(names_en[pokemon_id][1])
                identifier_forme = identifier
                try:
                    form_name = self._form_names[identifier][forme_id]
                except (KeyError, IndexError):
                    if forme_id != 0:
                        print(
                            identifier,
                            [i for i in forms_en if f"_{pokemon_id:0>3}_" in i[0]],
                        )
                        exit()
                    form_name = ""
                if form_name:
                    if not form_name.endswith("_"):
                        identifier += "-" + form_name
                    identifier_forme += "-" + form_name.strip("_")

                forme_pokemon_id = pokemon_id

                if not form_name.endswith("_") or forme_id == 0:
                    forme_pokemon_id = next(
                        (
                            int(i["id"])
                            for i in pokemon_csv.entries.values()
                            if i["identifier"] == identifier
                        ),
                        0,
                    )

                    # hardcode new zygarde ids
                    if identifier == "zygarde-50":
                        forme_pokemon_id = 718
                    if identifier == "zygarde-10-power-construct":
                        forme_pokemon_id = 10118
                    if identifier == "zygarde-50-power-construct":
                        forme_pokemon_id = 10119
                    if identifier == "zygarde-10":
                        forme_pokemon_id = 10181

                    if forme_pokemon_id == 0:
                        if forme_id == 0:
                            forme_pokemon_id = pokemon_id
                        else:
                            forme_pokemon_id = (
                                int(max(pokemon_csv.entries.keys())[0]) + 1
                            )

                    if "pokemon" in self._sections:
                        pokemon_csv.set_row(
                            id=forme_pokemon_id,
                            identifier=identifier,
                            species_id=pokemon_id,
                            height=forme.height // 10,
                            weight=forme.weight,
                            base_experience=forme.base_exp,
                            order_fallback_=10000,
                            is_default=int(forme_id == 0),
                        )

                        self._pokemon_evolutions(
                            pokemon_id, forme_pokemon_id, forme.evos
                        )

                        self._pokemon_stats(forme_pokemon_id, forme)
                        self._pokemon_types(forme_pokemon_id, forme)
                        self._pokemon_abilities(forme_pokemon_id, forme)
                    self._pokemon_moves(
                        forme_pokemon_id, forme, forme_index, pokemon_id, forme_id
                    )

                if "pokemon" in self._sections:
                    forme_pokemon_form_id = next(
                        (
                            int(i["id"])
                            for i in pokemon_forms_csv.entries.values()
                            if i["identifier"] == identifier_forme
                        ),
                        0,
                    )

                    # hardcode new zygarde ids
                    if identifier_forme == "zygarde-50":
                        forme_pokemon_form_id = 718
                    if identifier_forme == "zygarde-10-power-construct":
                        forme_pokemon_form_id = 10220
                    if identifier_forme == "zygarde-50-power-construct":
                        forme_pokemon_form_id = 10221
                    if identifier_forme == "zygarde-10":
                        forme_pokemon_form_id = 10340

                    if forme_pokemon_form_id == 0:
                        if forme_id == 0:
                            forme_pokemon_form_id = pokemon_id
                        else:
                            forme_pokemon_form_id = (
                                int(max(pokemon_forms_csv.entries.keys())[0]) + 1
                            )

                    is_default = int(forme_pokemon_id not in default_pokemon_list)
                    if identifier_forme.startswith("xerneas"):
                        is_default = int(identifier_forme == "xerneas-neutral")

                    if is_default:
                        default_pokemon_list.append(forme_pokemon_id)

                    pokemon_forms_csv.set_row(
                        id=forme_pokemon_form_id,
                        identifier=identifier_forme,
                        form_identifier=form_name.strip("_"),
                        pokemon_id=forme_pokemon_id,
                        introduced_in_version_group_id_fallback_=self._version_group_id,
                        is_default=is_default,
                        is_battle_only_fallback_=0,  # TODO
                        is_mega_fallback_=0,
                        form_order_fallback_=10000,
                        order_fallback_=10000,
                    )

                    if pokemon.forme_count > 1:
                        self._pokemon_form_names(
                            pokemon_id, forme_id, forme_pokemon_form_id
                        )

                    pokemon_form_generations_csv.set_row(
                        pokemon_form_id=forme_pokemon_form_id,
                        generation_id=self._generation_id,
                        game_index=0,
                    )

    def _pokemon_dex_numbers(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_dex_numbers_csv = self._open_csv("pokemon_dex_numbers")

        dex_ids = e = dict(zip(self._pokedex_identifiers, self._pokedex_ids))
        dex_numbers = {1: pokemon_id}
        dex_numbers.update({dex_ids[k]: v for k, v in pokemon.pokedex_numbers.items()})
        for pokedex_id, pokedex_number in dex_numbers.items():
            if pokedex_number:
                pokemon_dex_numbers_csv.set_row(
                    species_id=pokemon_id,
                    pokedex_id=pokedex_id,
                    pokedex_number=pokedex_number,
                )

    def _pokemon_abilities(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_abilities_csv = self._open_csv("pokemon_abilities")

        abilities = {1: pokemon.abilities[0]}
        if pokemon.abilities[1] not in abilities.values():
            abilities[2] = pokemon.abilities[1]
        if pokemon.abilities[2] not in abilities.values():
            abilities[3] = pokemon.abilities[2]
        for slot, ability in abilities.items():
            pokemon_abilities_csv.set_row(
                pokemon_id=pokemon_id,
                ability_id=ability,
                is_hidden=int(slot == 3),
                slot=slot,
            )

    def _pokemon_moves(
        self,
        forme_pokemon_id: int,
        pokemon: PersonalInfo,
        forme_index: int,
        pokemon_id: int,
        forme_id: int,
    ) -> None:
        learnset_table = self._open_table(LearnsetTable)
        egg_move_table = self._open_table(EggMoveTable)

        pokemon_moves_csv = self._open_csv("pokemon_moves")

        moves = set()

        # level-up
        learnset = learnset_table.get_info_from_index(forme_index)
        order = 0
        last_level = 0
        for i, (move_id, level) in enumerate(learnset.moves):
            if order > 0 and level == last_level:
                order += 1
            elif len(learnset.moves) > i + 1 and level == learnset.moves[i + 1][1]:
                order = 1
                last_level = level
            else:
                order = 0
                last_level = 0

            if (move_id, level) in moves:
                # some pokemon can learn a move two times at the same level
                # eg volcarona in sun/moon has quiver dance as a level 1 move both in
                # the first and sixth slot
                continue

            moves.add((move_id, level))

            pokemon_moves_csv.set_row(
                pokemon_id=forme_pokemon_id,
                version_group_id=self._version_group_id,
                move_id=move_id,
                pokemon_move_method_id=1,  # level-up
                level=level,
                order=order or "",
            )

        # egg
        if not egg_move_table._cls._SKIP:
            egg_moves = egg_move_table.get_info_from_index(pokemon_id)
            if forme_id > 0 and egg_moves.form_table_index is not None:
                egg_moves = egg_move_table.get_info_from_index(
                    egg_moves.form_table_index + forme_id - 1
                )

            for move_id in egg_moves.moves:
                pokemon_moves_csv.set_row(
                    pokemon_id=forme_pokemon_id,
                    version_group_id=self._version_group_id,
                    move_id=move_id,
                    pokemon_move_method_id=2,  # egg
                    level=0,
                    order="",
                )

        # tutor
        tutors = {
            int(self._type_tutors[i])
            for i, compatible in enumerate(pokemon.type_tutors)
            if compatible
        }

        for i, special_tutors in enumerate(pokemon.special_tutors):
            tutors.update(
                int(self._special_tutors[i][j])
                for j, compatible in enumerate(special_tutors)
                if compatible and self._special_tutors[i][j] > 0
            )

        if pokemon_id in self._hardcode_tutors:
            tutors.add(self._hardcode_tutors[pokemon_id])

        for move_id in tutors:
            if not move_id:
                continue
            pokemon_moves_csv.set_row(
                pokemon_id=forme_pokemon_id,
                version_group_id=self._version_group_id,
                move_id=move_id,
                pokemon_move_method_id=3,  # tutor
                level=0,
                order="",
            )

        # machine
        machines_csv = self._open_csv("machines")
        machines = {
            int(machines_csv.entries[k, self._version_group_id]["move_id"])
            for k, v in pokemon.tmhm.items()
            if v
        }
        for move_id in machines:
            pokemon_moves_csv.set_row(
                pokemon_id=forme_pokemon_id,
                version_group_id=self._version_group_id,
                move_id=move_id,
                pokemon_move_method_id=4,  # machine
                level=0,
                order="",
            )

        # form-change  # hardcoded
        special_forme_change_move = 0

        if forme_pokemon_id == 479:  # rotom
            special_forme_change_move = 84  # thunder-shock
        elif forme_pokemon_id == 10008:  # rotom-heat
            special_forme_change_move = 315  # overheat
        elif forme_pokemon_id == 10009:  # rotom-wash
            special_forme_change_move = 56  # hydro-pump
        elif forme_pokemon_id == 10010:  # rotom-frost
            special_forme_change_move = 59  # blizzard
        elif forme_pokemon_id == 10011:  # rotom-fan
            special_forme_change_move = 403  # air-slash
        elif forme_pokemon_id == 10012:  # rotom-mow
            special_forme_change_move = 437  # leaf-storm

        elif forme_pokemon_id == 10195:  # calyrex-ice
            special_forme_change_move = 824  # glacial-lance
        elif forme_pokemon_id == 10196:  # calyrex-shadow
            special_forme_change_move = 825  # astral-barrage

        if special_forme_change_move:
            pokemon_moves_csv.set_row(
                pokemon_id=forme_pokemon_id,
                version_group_id=self._version_group_id,
                move_id=special_forme_change_move,
                pokemon_move_method_id=10,  # form-change
                level=0,
                order="",
            )

    def _pokemon_egg_groups(self, pokemon_id: int, pokemon: PersonalInfo) -> None:
        pokemon_egg_groups_csv = self._open_csv("pokemon_egg_groups")

        for egg_group in pokemon.egg_groups:
            pokemon_egg_groups_csv.set_row(
                species_id=pokemon_id,
                egg_group_id=egg_group,
            )

    def _pokemon_evolutions(
        self, pokemon_id: int, forme_pokemon_id: int, evos: list[Evolution]
    ) -> None:
        # TODO: handle forme_pokemon_id
        pokemon_evolution_csv = self._open_csv("pokemon_evolution")

        for evo in evos:

            if evo.skip_record:
                continue

            trigger_id = evo.trigger_id
            trigger_item_id = str(
                self._get_item_id_from_game_index(evo.trigger_item_id) or ""
            )
            gender_id = str(evo.gender_id or "")

            if trigger_id == 4:
                if evo.species != 291:
                    print("non-ninjask shed")

                evolution_id = next(
                    (
                        k[0]
                        for k, v in pokemon_evolution_csv.entries.items()
                        if int(v["evolved_species_id"]) == 292  # shedinja
                        and int(v["evolution_trigger_id"]) == trigger_id
                    ),
                    int(max(pokemon_evolution_csv.entries.keys())[0]) + 1,
                )

                pokemon_evolution_csv.set_row(
                    id=evolution_id,
                    evolved_species_id=292,  # shedinja
                    evolution_trigger_id=trigger_id,
                    trigger_item_id="",
                    minimum_level="",
                    gender_id="",
                    held_item_id="",
                    time_of_day="",
                    known_move_id="",
                    known_move_type_id="",
                    minimum_happiness="",
                    minimum_beauty="",
                    relative_physical_stats="",
                    party_species_id="",
                    party_type_id="",
                    trade_species_id="",
                    needs_overworld_rain=0,
                    turn_upside_down=0,
                )

                trigger_id = 1

            if evo.species == 678:  # meowstic
                gender_id = ""
                if (372,) in pokemon_evolution_csv.entries and int(
                    pokemon_evolution_csv.entries[(372,)]["evolved_species_id"]
                ) == 678:
                    del pokemon_evolution_csv.entries[(372,)]

            evolution_id = next(
                (
                    k[0]
                    for k, v in pokemon_evolution_csv.entries.items()
                    if int(v["evolved_species_id"]) == evo.species
                    and int(v["evolution_trigger_id"]) == trigger_id
                    and v["trigger_item_id"] == trigger_item_id
                    and v["time_of_day"] == evo.time_of_day
                    # and int(v["location_id"]) == evo.location_id
                    and v["gender_id"] == gender_id
                    and bool(v["minimum_happiness"])
                    == bool(evo.minimum_happiness or "")
                    and v["minimum_beauty"]
                    == str(
                        evo.minimum_beauty or ""
                    )  # milotic has 2 minimum_beauty rows, one with 171 and the other with 170
                    and bool(v["minimum_affection"]) == False
                ),
                int(max(pokemon_evolution_csv.entries.keys())[0]) + 1,
            )

            pokemon_evolution_csv.set_row(
                id=evolution_id,
                evolved_species_id=evo.species,
                evolution_trigger_id=trigger_id,
                trigger_item_id=trigger_item_id,
                minimum_level=evo.level or "",
                gender_id=gender_id,
                # location_id=location_id,  # magnetic field, mossy stone, icy stone, mount lanakila
                held_item_id=self._get_item_id_from_game_index(evo.held_item_id) or "",
                time_of_day=evo.time_of_day,
                known_move_id=evo.known_move_id or "",
                known_move_type_id=evo.known_move_type_id or "",
                minimum_happiness=evo.minimum_happiness or "",
                minimum_beauty=evo.minimum_beauty or "",
                # minimum_affection=minimum_affection,  # affection doesn't exist anymore
                relative_physical_stats=evo.relative_physical_stats,
                party_species_id=evo.party_species_id or "",
                party_type_id=evo.party_type_id or "",
                trade_species_id=evo.trade_species_id or "",
                needs_overworld_rain=int(evo.needs_overworld_rain),
                turn_upside_down=int(evo.turn_upside_down),
            )

    def _create_evolution_chains(self) -> None:
        personal_table = self._open_table(PersonalTable)

        pokemon_species_csv = self._open_csv("pokemon_species")
        evolution_chains_csv = self._open_csv("evolution_chains")

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

            pokemon_id = int(key[0])
            pokemon = personal_table.get_info_from_index(pokemon_id)
            for forme_id in range(pokemon.forme_count):
                forme_index = pokemon.forme_index(pokemon_id, forme_id)
                forme = personal_table.get_info_from_index(forme_index)
                for evo in forme.evos:
                    pokemon_species_csv.set_row(
                        id=evo.species,
                        evolves_from_species_id=pokemon_id,
                        evolution_chain_id=entry["evolution_chain_id"],
                    )

    def _update_pokemon_order(self) -> None:
        pokemon_forms_csv = self._open_csv("pokemon_forms")
        pokemon_csv = self._open_csv("pokemon")
        pokemon_species_csv = self._open_csv("pokemon_species")

        # pokemon_forms
        ordered_pokemon_forms = sorted(
            [i[0] for i in pokemon_forms_csv.entries.keys() if int(i[0]) < 10000],
            key=lambda x: (
                int(pokemon_forms_csv.entries[(x,)]["order"]),
                int(pokemon_forms_csv.entries[(x,)]["id"]),
            ),
        )
        order = 0
        for pokemon_id in ordered_pokemon_forms:
            order += 1
            offset = 0
            if pokemon_id == 716:  # xerneas
                offset = 1
            elif pokemon_id == 666:  # vivillon
                offset = 6

            pokemon_forms_csv.entries[(pokemon_id,)]["order"] = str(order + offset)
            pokemon_forms_csv.entries[(pokemon_id,)]["form_order"] = str(1 + offset)

            ordered_alternate_formes = sorted(
                [
                    k[0]
                    for k, v in pokemon_forms_csv.entries.items()
                    if int(pokemon_csv.entries[(int(v["pokemon_id"]),)]["species_id"])
                    == pokemon_id
                    and k[0] != pokemon_id
                ],
                key=lambda x: (
                    # hardcode zygarde-10 order
                    (pokemon_forms_csv.entries[(x,)]["identifier"] != "zygarde-10"),
                    int(pokemon_forms_csv.entries[(x,)]["order"]),
                    int(pokemon_forms_csv.entries[(x,)]["id"]),
                ),
            )
            form_order = 1
            for pokemon_forme_id in ordered_alternate_formes:
                order += 1
                form_order += 1
                form_offset = int(offset >= form_order - 1)
                pokemon_forms_csv.entries[(pokemon_forme_id,)]["order"] = str(
                    order - form_offset
                )
                pokemon_forms_csv.entries[(pokemon_forme_id,)]["form_order"] = str(
                    form_order - form_offset
                )

        # pokemon
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
                    if int(v["species_id"]) == pokemon_id and k[0] != pokemon_id
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

        # pokemon_species
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

    def _dump_pokemon(self) -> None:
        personal_table = self._open_table(PersonalTable)

        pokemon_species_csv = self._open_csv("pokemon_species")

        names_en = self._open_text_file("English", "monsname")
        for pokemon_id in range(1, personal_table.max_id + 1):
            pokemon = personal_table.get_forme_entry(pokemon_id)
            if pokemon.is_present_in_game:
                identifier = to_id(names_en[pokemon_id][1])

                if "pokemon" in self._sections:
                    pokemon_species_csv.set_row(
                        id=pokemon_id,
                        identifier=identifier,
                        generation_id_fallback_=self._generation_id,
                        evolves_from_species_id_fallback_="_",
                        evolution_chain_id_fallback_="_",
                        color_id=pokemon.color,
                        shape_id_fallback_="",
                        habitat_id_fallback_="",  # it's a fr/lg thing
                        gender_rate=pokemon.gender_ratio,
                        capture_rate=pokemon.catch_rate,
                        base_happiness=pokemon.base_friendship,
                        is_baby=int(pokemon.is_baby),
                        hatch_counter=pokemon.hatch_cycles,
                        has_gender_differences_fallback_=0,  # TODO
                        growth_rate_id=pokemon.exp_growth,
                        forms_switchable_fallback_=0,  # TODO
                        is_legendary_fallback_=int(identifier in self._legendary_list),
                        is_mythical_fallback_=int(identifier in self._mythical_list),
                        order_fallback_=10000,
                        conquest_order_fallback_="",
                    )

                self._pokemon_formes(pokemon_id, pokemon)

                if "pokemon" in self._sections:
                    self._pokemon_species_names(pokemon_id)
                    self._pokemon_species_genera(pokemon_id)
                    self._pokemon_species_flavor_text(pokemon_id)

                    self._pokemon_dex_numbers(pokemon_id, pokemon)
                    self._pokemon_egg_groups(pokemon_id, pokemon)

        if "pokemon" in self._sections:
            self._create_evolution_chains()
            self._update_pokemon_order()


# TODO
# pokemon_items                         # wild held items

# locations/location_names
# location_areas/location_area_prose

# encounters SON TROPPI GUARDA DOPO
