from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemInfoSwSh(ItemInfo):
    _SIZE = 0x30
    _PATH = join("bin", "pml", "item", "item.dat")

    def __init__(self, table, path: str, item_id: int, data: bytes) -> None:
        super().__init__(table, path, item_id, data)

        self._price = read_as_int(2, self._data, 0x00)

        # 0x02 => 1 for tm20/tm28/tm44/tm52/tm59/tm83/tm92, 0 for everything else
        # sono tutte vendute alla battle tower, ma mancano 70/71/72

        # 0x03 => 0
        # 0x04 => bo son tanti non ho voglia, comunque non 0 ce l'hanno solo le tr, le palle, le pozioni, la pokedoll, e whishingpiece, forse i reward dei raid?
        # 0x05 => tr e wishing piece, forse anche questo reward dei raid?
        # 0x06 => 0
        # 0x07 => 0

        # 0x08 => bp/dynite-ore price
        """
        "premier-ball", 1       max-lair-dynite-ore
        "hp-up", 2              max-lair-dynite-ore    hammerlocke-bp-shop
        "protein", 2            max-lair-dynite-ore    hammerlocke-bp-shop
        "iron", 2               max-lair-dynite-ore    hammerlocke-bp-shop
        "carbos", 2             max-lair-dynite-ore    hammerlocke-bp-shop
        "calcium", 2            max-lair-dynite-ore    hammerlocke-bp-shop
        "rare-candy", 20                               hammerlocke-bp-shop
        "pp-up", 10                                    hammerlocke-bp-shop
        "zinc", 2               max-lair-dynite-ore    hammerlocke-bp-shop
        "white-herb", 15                                                                                   battle-tower-bp-shop-right
        "macho-brace", 10                              hammerlocke-bp-shop
        "mental-herb", 15                                                                                  battle-tower-bp-shop-right
        "choice-band", 25                                                                                  battle-tower-bp-shop-right
        "light-clay", 15                                                                                   battle-tower-bp-shop-right
        "life-orb", 25                                                                                     battle-tower-bp-shop-right
        "power-herb", 15                                                                                   battle-tower-bp-shop-right
        "toxic-orb", 10
        "flame-orb", 10
        "focus-sash", 15                                                                                   battle-tower-bp-shop-right
        "zoom-lens", 15
        "destiny-knot", 10                             hammerlocke-bp-shop
        "choice-scarf", 25                                                                                 battle-tower-bp-shop-right
        "power-bracer", 10                             hammerlocke-bp-shop
        "power-belt", 10                               hammerlocke-bp-shop
        "power-lens", 10                               hammerlocke-bp-shop
        "power-band", 10                               hammerlocke-bp-shop
        "power-anklet", 10                             hammerlocke-bp-shop
        "power-weight", 10                             hammerlocke-bp-shop
        "choice-specs", 25                                                                                 battle-tower-bp-shop-right
        "protector", 10                                hammerlocke-bp-shop
        "reaper-cloth", 10                             hammerlocke-bp-shop
        "razor-claw", 10                               hammerlocke-bp-shop
        "air-balloon", 15                                                                                  battle-tower-bp-shop-right
        "red-card", 20                                                                                     battle-tower-bp-shop-right
        "absorb-bulb", 10                                                                                  battle-tower-bp-shop-right
        "cell-battery", 10                                                                                 battle-tower-bp-shop-right
        "eject-button", 20                                                                                 battle-tower-bp-shop-right
        "weakness-policy", 20                                                                              battle-tower-bp-shop-right
        "assault-vest", 25                                                                                 battle-tower-bp-shop-right
        "ability-capsule", 50   max-lair-dynite-ore                                                        battle-tower-bp-shop-right
        "whipped-dream", 10                            hammerlocke-bp-shop
        "sachet", 10                                   hammerlocke-bp-shop
        "luminous-moss", 10                                                                                battle-tower-bp-shop-right
        "snowball", 10                                                                                     battle-tower-bp-shop-right
        "bottle-cap", 25        max-lair-dynite-ore                                                        battle-tower-bp-shop-right
        "adrenaline-orb", 10                                                                               battle-tower-bp-shop-right
        "beast-ball", 150       max-lair-dynite-ore
        "terrain-extender", 15                                                                             battle-tower-bp-shop-right
        "throat-spray", 10                                                                                 battle-tower-bp-shop-right
        "eject-pack", 20                                                                                   battle-tower-bp-shop-right
        "blunder-policy", 20                                                                               battle-tower-bp-shop-right
        "room-service", 15                                                                                 battle-tower-bp-shop-right
        "exp-candy-l", 1        max-lair-dynite-ore
        "exp-candy-xl", 3       max-lair-dynite-ore
        "dynamax-candy", 2      max-lair-dynite-ore
        "lonely-mint", 50                                                     battle-tower-bp-shop-left
        "adamant-mint", 50                                                    battle-tower-bp-shop-left
        "naughty-mint", 50                                                    battle-tower-bp-shop-left
        "brave-mint", 50                                                      battle-tower-bp-shop-left
        "bold-mint", 50                                                       battle-tower-bp-shop-left
        "impish-mint", 50                                                     battle-tower-bp-shop-left
        "lax-mint", 50                                                        battle-tower-bp-shop-left
        "relaxed-mint", 50                                                    battle-tower-bp-shop-left
        "modest-mint", 50                                                     battle-tower-bp-shop-left
        "mild-mint", 50                                                       battle-tower-bp-shop-left
        "rash-mint", 50                                                       battle-tower-bp-shop-left
        "quiet-mint", 50                                                      battle-tower-bp-shop-left
        "calm-mint", 50                                                       battle-tower-bp-shop-left
        "gentle-mint", 50                                                     battle-tower-bp-shop-left
        "careful-mint", 50                                                    battle-tower-bp-shop-left
        "sassy-mint", 50                                                      battle-tower-bp-shop-left
        "timid-mint", 50                                                      battle-tower-bp-shop-left
        "hasty-mint", 50                                                      battle-tower-bp-shop-left
        "jolly-mint", 50                                                      battle-tower-bp-shop-left
        "naive-mint", 50                                                      battle-tower-bp-shop-left
        "serious-mint", 50                                                    battle-tower-bp-shop-left
        "wishing-piece", 3      max-lair-dynite-ore
        "armorite-ore", 3       max-lair-dynite-ore
        "ability-patch", 200    max-lair-dynite-ore
        """

        # 0x09 => 0
        # 0x0A => 0
        # 0x0B => 0

        self.held_effect = int(self._data[0x0C])  # 0x02
        self.held_argument = int(self._data[0x0D])  # 0x03
        self.natural_gift_effect = int(self._data[0x0E])  # 0x04
        self.fling_effect = 0  # moved?
        self.fling_power = int(self._data[0x12])  # 0x06
        self.natural_gift_power = int(self._data[0x0F])  # 0x07
        self.packed = read_as_int(2, self._data, 0x10)  # 0x08

        self.effect_field = int(self._data[0x13])  # 0x0A
        self.effect_battle = int(self._data[0x14])  # 0x0B

        # 0x15 => 1 or 0

        # 0x16
        #  1 = healing items + vitamins + repels + ability capsule + ability patch + mints
        #  2 = evo strones + "useful?" held items (genesect's drives, toxic orb, choice band, amulet coin, ...)
        #  3 = apricorns + various food + ★-items + max honey + galarica twig/cuff/wreath + amorite/dynite ore
        #  4 = x-items + pokedoll + max mushrooms
        #  5 = balls
        #  6 = nothing
        #  7 = tm/tr
        #  8 = berries
        #  9 = key items
        # 10 = treasures + fossils
        # everything else is 255

        self._consumable = int(self._data[0x17])  # 0x0E
        self.sort_index = int(self._data[0x18])  # 0x0F

        # 0x19 => 0
        # 0x1A => ma che ne so è una sbrodolata infinita, ma tanti sono 0xFF
        # 0x1B => boh altra sbrodolata

        # 0x1C
        #  1 = balls
        #  2 = nothing
        #  3 = berries
        #  4 = tm/tr
        #  5 = normal gem

        # 0x1D => ordine o giù di lì (tm/tr/palle/bacche)

        self.cure_inflict = int(self._data[0x1E])  # 0x10
        self._boost_0 = int(self._data[0x1F])  # 0x11
        self._boost_1 = int(self._data[0x20])  # 0x12
        self._boost_2 = int(self._data[0x21])  # 0x13
        self._boost_3 = int(self._data[0x22])  # 0x14
        self.function_flags_0 = int(self._data[0x23])  # 0x15
        self.function_flags_1 = int(self._data[0x24])  # 0x16

        self.ev_hp = read_as_int(1, self._data, 0x25, True)  # 0x17
        self.ev_attack = read_as_int(1, self._data, 0x26, True)  # 0x18
        self.ev_defense = read_as_int(1, self._data, 0x27, True)  # 0x19
        self.ev_speed = read_as_int(1, self._data, 0x28, True)  # 0x1A
        self.ev_special_attack = read_as_int(1, self._data, 0x29, True)  # 0x1B
        self.ev_special_defense = read_as_int(1, self._data, 0x2A, True)  # 0x1C

        self.heal_amount = int(self._data[0x2B])  # 0x1D
        self.pp_gain = int(self._data[0x2C])  # 0x1E

        self.friendship_1 = read_as_int(1, self._data, 0x2D, True)  # 0x1F
        self.friendship_2 = read_as_int(1, self._data, 0x2E, True)  # 0x20
        self.friendship_3 = read_as_int(1, self._data, 0x2F, True)  # 0x21

    @property
    def fling_effect_id(self) -> int:
        return 0  # i have no idea
