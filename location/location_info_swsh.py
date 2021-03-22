from __future__ import annotations

import pickle

import re
import struct
from os.path import join

from base import BaseTable, T
from container.gfpack import GFPack
from text.text_file import TextFile
from utils import read_as_int

from .location_info import LocationInfo


def foo(cls_: type[T], table_: BaseTable) -> list[T]:
    table: list[T] = []

    path = join(table_._path, "bin", "archive", "field", "resident", "data_table.gfpak")

    pack = GFPack(path)

    games = ["k", "t"]
    encounter_types = {"symbol": "symbol_", "hidden": ""}

    for game_id, game in enumerate(games):
        n = 0
        for encounter_type_id, encounter_type in encounter_types.items():
            data = EncounterArchive8(
                pack.get_data_file_name(f"encount_{encounter_type}{game}.bin")
            )

            for encounter_table_id, encounter_table in enumerate(data.encounter_tables):
                """
                Clear
                Cloudy
                Rain
                Thunderstorm
                Harsh sunlight
                Snow
                Blizzard
                Sandstorm
                Fog
                """
                for sub_table in encounter_table.sub_tables:
                    for slot in sub_table.slots:
                        table.append(
                            cls_(
                                table_,
                                table_._path,
                                n,
                                pickle.dumps(
                                    (
                                        game_id,
                                        encounter_type_id,
                                        encounter_table_id,
                                        encounter_table,
                                        sub_table,
                                        slot,
                                    )
                                ),
                            )
                        )
                        n += 1

    return table


class LocationInfoSwSh(LocationInfo):
    _TYPE = "gfpak"
    _SIZE = 2
    _MAX_ID = 59
    _PATH = join("bin", "archive", "field", "resident", "data_table.gfpak")

    _CUSTOM_FUNCTION = foo

    _AREAS = {
        14802856697865334578: "route-1",
        16098238665042709457: "route-2",
        15421084501918781308: "rolling-fields",
        5011552708176933765: "dappled-grove",
        16289074425614718930: "watchtower-ruins",
        17216887570387488947: "east-lake-axewell",
        17929363551360786336: "west-lake-axewell",
        13173003681479064953: "axews-eye",
        5912537832360617158: "south-lake-miloch",
        13578976987769047095: "giants-seat",
        13149508635596856885: "north-lake-miloch",
        15749386318250586093: "west-lake-axewell-(surfing)",
        8941856495303103811: "south-lake-miloch-(surfing)",
        14704123330686007468: "east-lake-axewell-(surfing)",
        10079889490518145934: "north-lake-miloch-(surfing)",
        1045840894587918384: "route-3",
        9414672940960288855: "galar-mine",
        6569559496175043255: "route-4",
        10189437501796725438: "route-5",
        1644654201196140709: "galar-mine-no-2",
        4426291493402335070: "motostoke-outskirts",
        7684920403895300377: "motostoke-riverbank",
        3937795978280443506: "bridge-field",
        16502105383608088157: "route-6",
        2314560941659991409: "glimwood-tangle",
        4769635905126557068: "route-7",
        1987678989857518099: "route-8",
        12311367809796800138: "route-8-(on-steamdrift-way)",
        10454739454557740273: "route-9",
        14831397447773609575: "route-9-(in-circhester-bay)",
        6501948272446742616: "route-9-(in-outer-spikemuth)",
        12191527771748010389: "route-9--(surfing)",
        108405602218038304: "route-10-(near-station)",
        2238037095669842726: "stony-wilderness",
        12470946702421681709: "dusty-bowl",
        14814337755417356964: "giants-mirror",
        14792181135656930299: "hammerlocke-hills",
        8155790597580268538: "giants-cap",
        6427083574832360289: "lake-of-outrage",
        17842673694954292531: "route-10",
        11703243092075141866: "route-2-(high-level)",
        6221736718999807588: "route-3-(garbage)",
        14643734168574114136: "rolling-fields-(flying)",
        2240344234067201080: "rolling-fields-(ground)",
        2522425990829471975: "rolling-fields-(2)",
        17418316618293521434: "watchtower-ruins-(flying)",
        4408589107970661557: "east-lake-axewell-(flying)",
        7931431154911383326: "east-lake-axewell-(flying)",
        3562805552886284654: "south-lake-miloch-(flying)",
        1841479819421998575: "south-lake-miloch-(2)",
        18064431298369352138: "motostoke-riverbank-(surfing)",
        13400298986890128391: "bridge-field-(surfing)",
        6867438244088508730: "bridge-field-(flying)",
        17727257354609754346: "stony-wilderness-(2)",
        8569873078348691278: "stony-wilderness-(flying)",
        4550407417029347252: "giants-mirror-(flying)",
        3281006592064076186: "dusty-bowl-(flying)",
        3163750874897894432: "giants-mirror-(ground)",
        4174862175178802468: "dusty-bowl-and-giants-mirror-(surfing)",
        12828081038216775610: "giants-cap-(ground)",
        5240310184801093813: "stony-wilderness-(3)",
        13075475323264852449: "giants-cap-(2)",
        8842885044989189611: "giants-cap-(3)",
        15848037920045234858: "giants-cap-(ground)",
        463756380035858989: "hammerlocke-hills-(flying)",
        9775479704314998002: "lake-of-outrage-(surfing)",
        10675943465615381036: "slumbering-weald-(low-level)",
        6702184572991014702: "slumbering-weald-(high-level)",
        11859196656005774847: "route-2-(surfing)",
        12398840687885707347: "route-9-(in-circhester-bay)-(surfing)",
        5934904140307748868: "fields-of-honor",
        12709739045338108041: "fields-of-honor-(surfing)",
        10498402293877004401: "fields-of-honor-(beach)",
        14144082032569836332: "loop-lagoon-(beach)",
        7486107453753719673: "training-lowlands-(beach)",
        2825608396065455376: "challenge-beach-(beach)",
        15426379945819217504: "challenge-beach-(surfing---river)",
        13748528842966731895: "soothing-wetlands",
        2019051580140822632: "soothing-wetlands-(puddles)",
        13547547800739091462: "forest-of-focus",
        3651162541370367107: "forest-of-focus-(surfing)",
        4165961899686550721: "challenge-beach",
        4322086548357726930: "challenge-beach-(surfing---ocean)",
        3106910795852394024: "brawlers-cave",
        3962747355158076597: "brawlers-cave-(surfing)",
        13522648993351680091: "challenge-road",
        18129943810681718490: "courageous-cavern",
        13550793625090617295: "courageous-cavern-(surfing)",
        12407083334307401669: "loop-lagoon",
        9020182694154211041: "loop-lagoon-(surfing)",
        9647421614796991420: "training-lowlands",
        10799954969281615446: "warm-up-tunnel",
        12102462448244659591: "potbottom-desert",
        3506854014308116510: "workout-sea",
        8031196072131133484: "workout-sea-(surfing)",
        17510959427842118501: "stepping-stone-sea",
        10926823860330060545: "stepping-stone-sea-(surfing)",
        15987770470958979932: "insular-sea",
        18130282878634645722: "insular-sea-(surfing)",
        13937548113001578119: "honeycalm-sea-(surfing)",
        584763124368904881: "honeycalm-island",
        9723200442135696725: "honeycalm-island-(surfing)",
        4155538272100726559: "training-lowlands-(surfing)",
        10864549973671932803: "stepping-stone-sea-(sharpedo)",
        14496249600837470090: "insular-sea-(sharpedo)",
        17086542030004667341: "workout-sea-(sharpedo)",
        11241065844363663652: "honeycalm-sea-(sharpedo)",
        15486258318313299541: "slippery-slope",
        12535231422909319391: "frostpoint-field",
        3498275149160305136: "giants-bed",
        5829771149564166217: "old-cemetery",
        14052094005327180578: "snowslide-slope",
        13215925304149983427: "tunnel-to-the-top",
        18210176436701687956: "path-to-the-peak",
        11764886137958196851: "giants-foot",
        16476844204871348882: "roaring-sea-caves",
        1777506031753476153: "frigid-sea",
        4523580897772426336: "three-point-pass",
        16510864269492660043: "ballimere-lake",
        3394378558111045976: "lakeside-cave",
        17916902384401718958: "giants-bed--giants-foot-(surfing)",
        6185960335969839287: "roaring-sea-caves-(surfing)",
        8670380455920256077: "frigid-sea-(surfing)",
        11231252969804454463: "ballimere-lake-(surfing)",
        543741481431955524: "route-1",
        1167944128207368373: "route-2",
        8603975842942699582: "rolling-fields",
        8603976942454327793: "dappled-grove",
        8603978041965956004: "watchtower-ruins",
        8603979141477584215: "east-lake-axewell",
        8603980240989212426: "west-lake-axewell",
        8603981340500840637: "axews-eye",
        8603964847826417472: "south-lake-miloch",
        8603965947338045683: "giants-seat",
        8604965403407900257: "north-lake-miloch",
        1822717596287504666: "route-3",
        8605958262407985565: "motostoke-riverbank",
        8605954963873100932: "bridge-field",
        15838980664796950643: "route-4",
        10333453570355353198: "slumbering-weald",
        16201389492170519719: "city-of-motostoke",
        16493754132877086936: "route-5",
        2049508092492223717: "town-of-hulbury",
        9023940719055555153: "galar-mine-no-2",
        8491605567333890387: "galar-mine",
        9023937420520670520: "motostoke-outskirts",
        12144730752072092565: "glimwood-tangle",
        17148637552120044329: "route-6",
        17680969405306824462: "route-7",
        4943510927838926711: "route-8",
        5475807596653604092: "route-8-(on-steamdrift-way)",
        5475810895188488725: "route-9",
        5475804298118719459: "route-9-(in-circhester-bay)",
        5475809795676860514: "route-9-(in-outer-spikemuth)",
        12912544744327468170: "route-10-(near-station)",
        8606912638501083488: "stony-wilderness",
        8606915937035968121: "dusty-bowl",
        8606914837524339910: "giants-mirror",
        8606918136059224543: "hammerlocke-hills",
        8606917036547596332: "giants-cap",
        8606920335082480965: "lake-of-outrage",
        1167940829672483740: "route-2",
        12912543644815839959: "route-10",
        10333451371332096776: "slumbering-weald",
        10415247527101297894: "fields-of-honor",
        10415246427589669683: "soothing-wetlands",
        10415245328078041472: "forest-of-focus",
        10415253024659438949: "challenge-beach",
        10415250825636182527: "challenge-road",
        10415249726124554316: "courageous-cavern",
        10415257422705951793: "loop-lagoon",
        10415256323194323582: "training-lowlands",
        10417231046078212088: "workout-sea",
        10417234344613096721: "stepping-stone-sea",
        10417233245101468510: "insular-sea",
        10417236543636353143: "honeycalm-sea",
        10416241485613011413: "honeycalm-island",
        9791190015860808897: "slippery-slope",
        9791187816837552475: "frostpoint-field",
        9791193314395693530: "giants-bed",
        9791194413907321741: "old-cemetery",
        9791191115372437108: "snowslide-slope",
        9792039938349226775: "giants-foot",
        9792042137372483197: "frigid-sea",
        9792041037860854986: "three-point-pass",
        9789206496883894703: "ballimere-lake",
    }

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._data = pickle.loads(data)

        self.game_id = self._data[0]
        self.encounter_type_id = self._data[1]
        self.encounter_table_id = self._data[2]
        self._encounter_table = self._data[3]
        self._sub_table = self._data[4]
        self._slot = self._data[5]

        self.zone_id = self._encounter_table.zone_id
        self.level_min = self._sub_table.level_min
        self.level_max = self._sub_table.level_max
        self.probability = self._slot.probability
        self.species = self._slot.species
        self.form = self._slot.form
