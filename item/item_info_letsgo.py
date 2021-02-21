from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemInfoLetsGo(ItemInfo):
    _SIZE = None
    _MAX_ITEM_ID = 1057
    _PATH = join("bin", "pokelib", "item", "item{item_id:0>3}.dat")

    def __init__(self, table, path: str, item_id: int, data: bytes) -> None:
        super().__init__(table, path, item_id, data)

        self._price = read_as_int(2, self._data, 0x00) * 10

        self.held_effect = int(self._data[0x02])
        self.held_argument = int(self._data[0x03])
        self.natural_gift_effect = int(self._data[0x04])
        self.fling_effect = int(self._data[0x05])
        self.fling_power = int(self._data[0x06])
        self.natural_gift_power = int(self._data[0x07])
        self.packed = read_as_int(2, self._data, 0x08)

        self.effect_field = int(self._data[0x0A])
        self.effect_battle = int(self._data[0x0B])

        # 0x0C => balls = 2, lots of things = 1, everything else = 0

        # 0x0D
        #  0 = main menu items (let's go)
        #  1 = healing items + vitamins + repels + ability capsule + ability patch + mints
        #  2 = evo strones + "useful?" items + pokemon candies + pokedoll + misc
        #  3 = x-items
        #  4 = key items
        #  5 = balls
        #  6 = mail
        #  7 = tm/hm
        #  8 = berries
        #  9 = battle items (incl. megastones, z-crystals)
        # 10 = treasures + fossils
        # everything else is 255

        self._consumable = int(self._data[0x0E])
        self.sort_index = int(self._data[0x0F])
        self.cure_inflict = int(self._data[0x10])
        self._boost_0 = int(self._data[0x11])
        self._boost_1 = int(self._data[0x12])
        self._boost_2 = int(self._data[0x13])
        self._boost_3 = int(self._data[0x14])
        self.function_flags_0 = int(self._data[0x15])
        self.function_flags_1 = int(self._data[0x16])

        self.ev_hp = read_as_int(1, self._data, 0x17, True)
        self.ev_attack = read_as_int(1, self._data, 0x18, True)
        self.ev_defense = read_as_int(1, self._data, 0x19, True)
        self.ev_speed = read_as_int(1, self._data, 0x1A, True)
        self.ev_special_attack = read_as_int(1, self._data, 0x1B, True)
        self.ev_special_defense = read_as_int(1, self._data, 0x1C, True)

        self.heal_amount = int(self._data[0x1D])
        self.pp_gain = int(self._data[0x1E])

        self.friendship_1 = read_as_int(1, self._data, 0x1F, True)
        self.friendship_2 = read_as_int(1, self._data, 0x20, True)
        self.friendship_3 = read_as_int(1, self._data, 0x21, True)

        # 0x22 => 0
        # 0x23 => 0
