from __future__ import annotations

from utils import read_as_int


class ItemInfo:
    _SIZE: int | None
    _MAX_ITEM_ID: int
    _PATH: str

    def __init__(self, table, path: str, item_id: int, data: bytes) -> None:
        self._table = table
        self._path = path
        self._id = item_id
        self._data = data

        self._price = read_as_int(2, self._data, 0x00)

        self.held_effect = int(self._data[0x02])
        self.held_argument = int(self._data[0x03])
        self.natural_gift_effect = int(self._data[0x04])
        self.fling_effect = int(self._data[0x05])
        self.fling_power = int(self._data[0x06])
        self.natural_gift_power = int(self._data[0x07])
        self.packed = read_as_int(2, self._data, 0x08)

        # Routine # to call when used; 0=unusable.
        self.effect_field = int(self._data[0x0A])
        self.effect_battle = int(self._data[0x0B])

        self.unk_0xC = int(self._data[0x0C])  # 0 or 1
        self.unk_0xD = int(
            self._data[0x0D]
        )  # Classification (0-3 Battle, 4 Balls, 5 Mail)
        self._consumable = int(self._data[0x0E])
        self.sort_index = int(self._data[0x0F])
        self.cure_inflict = int(
            self._data[0x10]
        )  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Item/BattleStatusFlags.cs
        self._boost_0 = int(
            self._data[0x11]
        )  # Revive 1, Sacred Ash 3, Rare Candy 5, EvoStone 8, upper4 for BoostAtk
        self._boost_1 = int(self._data[0x12])  # DEF, SPA
        self._boost_2 = int(self._data[0x13])  # SPD, SPE
        self._boost_3 = int(self._data[0x14])  # ACC, CRIT PPUpFlags
        self.function_flags_0 = int(
            self._data[0x15]
        )  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Item/ItemFlags1.cs
        self.function_flags_1 = int(
            self._data[0x16]
        )  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Item/ItemFlags2.cs

        self.ev_hp = read_as_int(1, self._data, 0x17, True)
        self.ev_attack = read_as_int(1, self._data, 0x18, True)
        self.ev_defense = read_as_int(1, self._data, 0x19, True)
        self.ev_speed = read_as_int(1, self._data, 0x1A, True)
        self.ev_special_attack = read_as_int(1, self._data, 0x1B, True)
        self.ev_special_defense = read_as_int(1, self._data, 0x1C, True)

        self.heal_amount = int(
            self._data[0x1D]
        )  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Misc/Heal.cs
        self.pp_gain = int(self._data[0x1E])

        self.friendship_1 = read_as_int(1, self._data, 0x1F, True)
        self.friendship_2 = read_as_int(1, self._data, 0x20, True)
        self.friendship_3 = read_as_int(1, self._data, 0x21, True)
        # public byte _0x23, _0x24;

    @property
    def buy_price(self) -> int:
        return self._price * 10

    @property
    def sell_price(self) -> int:
        return self._price * 5

    @property
    def natural_gift_type(self) -> int:
        return self.packed & 0x1F

    @property
    def flag_1(self) -> bool:
        return bool((self.packed >> 5) & 0x1)

    @property
    def flag_2(self) -> bool:
        return bool((self.packed >> 6) & 0x1)

    @property
    def pocket_field(self) -> int:
        return (self.packed >> 7) & 0x0F

    @property
    def pocket_battle(self) -> int:
        return (
            self.packed >> 11
        )  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Item/BattlePocket.cs

    @property
    def revive(self) -> bool:
        return not bool((self._boost_0 >> 0) & 0x1)

    @property
    def revive_all(self) -> bool:
        return bool((self._boost_0 >> 1) & 0x1)

    @property
    def level_up(self) -> bool:
        return bool((self._boost_0 >> 2) & 0x1)

    @property
    def evo_stone(self) -> bool:
        return bool((self._boost_0 >> 3) & 0x1)

    @property
    def boost_attack(self) -> int:
        return self._boost_0 >> 4

    @property
    def boost_defense(self) -> int:
        return self._boost_1 & 0x0F

    @property
    def boost_special_attack(self) -> int:
        return self._boost_1 >> 4

    @property
    def boost_special_defense(self) -> int:
        return self._boost_2 & 0x0F

    @property
    def boost_speed(self) -> int:
        return self._boost_2 >> 4

    @property
    def boost_accuracy(self) -> int:
        return self._boost_3 & 0x0F

    @property
    def boost_crit(self) -> int:
        return (self._boost_3 >> 4) & 0x3

    @property
    def boost_pp(self) -> bool:
        return bool((self._boost_3 >> 6) & 1)

    @property
    def boost_pp_max(self) -> bool:
        return bool((self._boost_3 >> 7) & 1)

    @property
    def use_consume(self) -> bool:
        return self._consumable & 0x0F != 0

    @property
    def use_keep(self) -> bool:
        return self._consumable & 0xF0 != 0

    @property
    def pouch_id(self) -> int:
        return int(self._data[0x11] & 0x0F)

    @property
    def pouch(self) -> int:
        return {
            0: 2,
            1: 3,
            2: 7,
            3: 5,
            4: 1,  # items => misc?
            5: 4,
            6: 0,  # treasures
            7: 0,  # ingredients
            8: 8,
        }[self.pouch_id]

    @property
    def item_sprite(self) -> int:
        return read_as_int(2, self._data, 0x1A)

    @property
    def group_type(self) -> int:
        return int(self._data[0x1C])

    @property
    def group_index(self) -> int:
        return int(self._data[0x1D])

    ################

    @property
    def fling_effect_id(self) -> int:
        effects = {i + 1: 3 for i in range(23)}  # berries => berry-effect
        effects.update(
            {
                24: 4,  # white-herb => herb-effect
                25: 4,  # mental-herb => herb-effect
                26: 7,  # kings-rock/razor-fang => flinch
                27: 5,  # light-ball => paralyze
                28: 6,  # poison-barb => poison
                29: 1,  # toxic-orb => badly-poison
                30: 2,  # flame-orb => burn
                0: 0,  # no-effect
            }
        )
        return effects[self.fling_effect]
