from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemInfoLetsGo(ItemInfo):
    _TYPE = "multiplefiles"
    _MAX_ID = 1057
    _PATH = join("bin", "pokelib", "item", "item{id:0>3}.dat")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

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

        self._pocket = int(self._data[0x0D])

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

    def category_id(self, identifier: str) -> int:
        if self._pocket == 0:  # main menu items
            return 23  # key => unused

        if self._pocket == 1:  # healing items + vitamins + repels + ability capsule
            if identifier == "pewter-crunchies":
                return 30  # medicine => status-cures

        if (
            self._pocket == 2
        ):  # evo stones + "useful?" items + pokemon candies + pokedoll + misc
            if identifier.replace("-l", "").replace("-xl", "") in (
                "health-candy",
                "mighty-candy",
                "tough-candy",
                "smart-candy",
                "courage-candy",
                "quick-candy",
            ):
                return 26  # medicine => vitamins
            if identifier.endswith("-candy"):
                return 47  # misc => species-candy
            if identifier.endswith("lure"):
                return 11  # misc => spelunking

        if self._pocket == 4:  # key
            if identifier in (
                "secret-key--letsgo",
                "ss-ticket--letsgo",
                "parcel--letsgo",
                "card-key--letsgo",
            ):
                return 22  # plot-advancement
            if identifier == "autograph":
                return 23  # unused

        if self._pocket == 8:
            if identifier[:7] in ("golden-", "silver-") and identifier[-6:] == "-berry":
                return 48  # berries => catching-bonus

        if self._pocket == 10:  # treasures
            if identifier in (
                "stretchy-spring",
                "chalky-stone",
                "marble",
                "lone-earring",
                "beach-glass",
                "gold-leaf",
                "silver-leaf",
                "polished-mud-ball",
                "tropical-shell",
                "leaf-letter--pikachu",
                "leaf-letter--eevee",
                "small-bouquet",
            ):
                return 24  # misc => loot

        print("no category_id: ", self._pocket, identifier)
        return 0
