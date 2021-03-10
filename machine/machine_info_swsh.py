from __future__ import annotations

import re
import struct
from os.path import join

from base import BaseTable, T
from text.text_file import TextFile
from utils import read_as_int

from .machine_info import MachineInfo


def match_machine_move(cls_: type[T], table_: BaseTable) -> list[T]:
    table = []

    item_names = [
        (int(k[k.find("_") + 1 :]), v)
        for k, v in TextFile(table_._path, "English", "itemname", "swsh").lines
        if re.match(r"^T[RM]\d\d$", v)
    ]
    # item_names.sort(key=lambda x: (x[1][:2], x[1][2:] == "00", x[1][2:]))
    item_names.sort(key=lambda x: x[1])
    move_names = [
        (int(k[k.find("_") + 1 :]), v)
        for k, v in TextFile(table_._path, "English", "wazaname", "swsh").lines
    ]
    languages = [
        "JPN",
        "Korean",
        "Trad_Chinese",
        "French",
        "German",
        "Spanish",
        "Italian",
        "English",
        "JPN_KANJI",
        "Simp_Chinese",
    ]
    item_descriptions = {}
    move_descriptions = {}
    for lang in languages:
        item_descriptions[lang] = {
            int(k[k.find("_") + 1 :]): v
            for k, v in TextFile(table_._path, lang, "iteminfo", "swsh").lines
        }
        move_descriptions[lang] = [
            (int(k[k.find("_") + 1 :]), v)
            for k, v in TextFile(table_._path, lang, "wazainfo", "swsh").lines
        ]

    n = 0
    for item_name in item_names:
        for lang in languages:
            item_desc = item_descriptions[lang][item_name[0]]
            moves = [
                k
                for k, v in move_descriptions[lang]
                if v.replace(" \n", "\n") == item_desc
            ]
            if len(moves) == 1:
                move_id = moves[0]
                break
        else:
            try:
                move_id = {
                    "TM25": 182,  # protect (conflicts with detect and max-guard)
                    "TR22": 188,  # sludge-bomb (conflicts with sludge)
                    "TR25": 473,  # psyshock (conflicts with psystrike)
                }[item_name[1]]
            except:
                print(item_name[1], moves)
                continue

        if move_names[move_id][1] != EXPECTED_TMS_TRS[item_name[1]]:
            print(
                f"{item_name[1]}: got {move_names[move_id][1]}, expected {EXPECTED_TMS_TRS[item_name[1]]}"
            )

        table.append(cls_(table_, table_._path, n, struct.pack("<H", move_id)))
        n += 1

    return table


class MachineInfoSwSh(MachineInfo):
    _CUSTOM_FUNCTION = match_machine_move

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.machine_number = id
        machine_type = "tm" if self.machine_number < 100 else "tr"
        self.machine_name = f"{machine_type}{str(self.machine_number + 1)[-2:]:0>2}"
        self.move_id = read_as_int(2, self._data)


EXPECTED_TMS_TRS = {
    "TM00": "Mega Punch",
    "TM01": "Mega Kick",
    "TM02": "Pay Day",
    "TM03": "Fire Punch",
    "TM04": "Ice Punch",
    "TM05": "Thunder Punch",
    "TM06": "Fly",
    "TM07": "Pin Missile",
    "TM08": "Hyper Beam",
    "TM09": "Giga Impact",
    "TM10": "Magical Leaf",
    "TM11": "Solar Beam",
    "TM12": "Solar Blade",
    "TM13": "Fire Spin",
    "TM14": "Thunder Wave",
    "TM15": "Dig",
    "TM16": "Screech",
    "TM17": "Light Screen",
    "TM18": "Reflect",
    "TM19": "Safeguard",
    "TM20": "Self-Destruct",
    "TM21": "Rest",
    "TM22": "Rock Slide",
    "TM23": "Thief",
    "TM24": "Snore",
    "TM25": "Protect",
    "TM26": "Scary Face",
    "TM27": "Icy Wind",
    "TM28": "Giga Drain",
    "TM29": "Charm",
    "TM30": "Steel Wing",
    "TM31": "Attract",
    "TM32": "Sandstorm",
    "TM33": "Rain Dance",
    "TM34": "Sunny Day",
    "TM35": "Hail",
    "TM36": "Whirlpool",
    "TM37": "Beat Up",
    "TM38": "Will-O-Wisp",
    "TM39": "Facade",
    "TM40": "Swift",
    "TM41": "Helping Hand",
    "TM42": "Revenge",
    "TM43": "Brick Break",
    "TM44": "Imprison",
    "TM45": "Dive",
    "TM46": "Weather Ball",
    "TM47": "Fake Tears",
    "TM48": "Rock Tomb",
    "TM49": "Sand Tomb",
    "TM50": "Bullet Seed",
    "TM51": "Icicle Spear",
    "TM52": "Bounce",
    "TM53": "Mud Shot",
    "TM54": "Rock Blast",
    "TM55": "Brine",
    "TM56": "U-turn",
    "TM57": "Payback",
    "TM58": "Assurance",
    "TM59": "Fling",
    "TM60": "Power Swap",
    "TM61": "Guard Swap",
    "TM62": "Speed Swap",
    "TM63": "Drain Punch",
    "TM64": "Avalanche",
    "TM65": "Shadow Claw",
    "TM66": "Thunder Fang",
    "TM67": "Ice Fang",
    "TM68": "Fire Fang",
    "TM69": "Psycho Cut",
    "TM70": "Trick Room",
    "TM71": "Wonder Room",
    "TM72": "Magic Room",
    "TM73": "Cross Poison",
    "TM74": "Venoshock",
    "TM75": "Low Sweep",
    "TM76": "Round",
    "TM77": "Hex",
    "TM78": "Acrobatics",
    "TM79": "Retaliate",
    "TM80": "Volt Switch",
    "TM81": "Bulldoze",
    "TM82": "Electroweb",
    "TM83": "Razor Shell",
    "TM84": "Tail Slap",
    "TM85": "Snarl",
    "TM86": "Phantom Force",
    "TM87": "Draining Kiss",
    "TM88": "Grassy Terrain",
    "TM89": "Misty Terrain",
    "TM90": "Electric Terrain",
    "TM91": "Psychic Terrain",
    "TM92": "Mystical Fire",
    "TM93": "Eerie Impulse",
    "TM94": "False Swipe",
    "TM95": "Air Slash",
    "TM96": "Smart Strike",
    "TM97": "Brutal Swing",
    "TM98": "Stomping Tantrum",
    "TM99": "Breaking Swipe",
    "TR00": "Swords Dance",
    "TR01": "Body Slam",
    "TR02": "Flamethrower",
    "TR03": "Hydro Pump",
    "TR04": "Surf",
    "TR05": "Ice Beam",
    "TR06": "Blizzard",
    "TR07": "Low Kick",
    "TR08": "Thunderbolt",
    "TR09": "Thunder",
    "TR10": "Earthquake",
    "TR11": "Psychic",
    "TR12": "Agility",
    "TR13": "Focus Energy",
    "TR14": "Metronome",
    "TR15": "Fire Blast",
    "TR16": "Waterfall",
    "TR17": "Amnesia",
    "TR18": "Leech Life",
    "TR19": "Tri Attack",
    "TR20": "Substitute",
    "TR21": "Reversal",
    "TR22": "Sludge Bomb",
    "TR23": "Spikes",
    "TR24": "Outrage",
    "TR25": "Psyshock",
    "TR26": "Endure",
    "TR27": "Sleep Talk",
    "TR28": "Megahorn",
    "TR29": "Baton Pass",
    "TR30": "Encore",
    "TR31": "Iron Tail",
    "TR32": "Crunch",
    "TR33": "Shadow Ball",
    "TR34": "Future Sight",
    "TR35": "Uproar",
    "TR36": "Heat Wave",
    "TR37": "Taunt",
    "TR38": "Trick",
    "TR39": "Superpower",
    "TR40": "Skill Swap",
    "TR41": "Blaze Kick",
    "TR42": "Hyper Voice",
    "TR43": "Overheat",
    "TR44": "Cosmic Power",
    "TR45": "Muddy Water",
    "TR46": "Iron Defense",
    "TR47": "Dragon Claw",
    "TR48": "Bulk Up",
    "TR49": "Calm Mind",
    "TR50": "Leaf Blade",
    "TR51": "Dragon Dance",
    "TR52": "Gyro Ball",
    "TR53": "Close Combat",
    "TR54": "Toxic Spikes",
    "TR55": "Flare Blitz",
    "TR56": "Aura Sphere",
    "TR57": "Poison Jab",
    "TR58": "Dark Pulse",
    "TR59": "Seed Bomb",
    "TR60": "X-Scissor",
    "TR61": "Bug Buzz",
    "TR62": "Dragon Pulse",
    "TR63": "Power Gem",
    "TR64": "Focus Blast",
    "TR65": "Energy Ball",
    "TR66": "Brave Bird",
    "TR67": "Earth Power",
    "TR68": "Nasty Plot",
    "TR69": "Zen Headbutt",
    "TR70": "Flash Cannon",
    "TR71": "Leaf Storm",
    "TR72": "Power Whip",
    "TR73": "Gunk Shot",
    "TR74": "Iron Head",
    "TR75": "Stone Edge",
    "TR76": "Stealth Rock",
    "TR77": "Grass Knot",
    "TR78": "Sludge Wave",
    "TR79": "Heavy Slam",
    "TR80": "Electro Ball",
    "TR81": "Foul Play",
    "TR82": "Stored Power",
    "TR83": "Ally Switch",
    "TR84": "Scald",
    "TR85": "Work Up",
    "TR86": "Wild Charge",
    "TR87": "Drill Run",
    "TR88": "Heat Crash",
    "TR89": "Hurricane",
    "TR90": "Play Rough",
    "TR91": "Venom Drench",
    "TR92": "Dazzling Gleam",
    "TR93": "Darkest Lariat",
    "TR94": "High Horsepower",
    "TR95": "Throat Chop",
    "TR96": "Pollen Puff",
    "TR97": "Psychic Fangs",
    "TR98": "Liquidation",
    "TR99": "Body Press",
}
