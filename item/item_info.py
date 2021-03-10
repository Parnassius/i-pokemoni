from __future__ import annotations

from base import BaseInfo
from utils import read_as_int


class ItemInfo(BaseInfo):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._price: int

        self.held_effect: int
        self.held_argument: int
        self.natural_gift_effect: int
        self.fling_effect: int
        self.fling_power: int
        self.natural_gift_power: int
        self.packed: int

        # Routine # to call when used; 0=unusable.
        self.effect_field: int
        self.effect_battle: int

        self._consumable: int
        self.sort_index: int
        self.cure_inflict: int  # sleep poison burn freeze paralysis confusion infatuation guard_spec
        self._boost_0: int  # revive revive_all rare_exp_candy evo_stone attack(4)
        self._boost_1: int  # defense(4) special_attack(4)
        self._boost_2: int  # special_defense(4) speed(4)
        self._boost_3: int  # accuracy(4) crit(2) pp_up pp_max
        self.function_flags_0: int  # restore_pp restore_pp_all restore_hp add_ev_hp add_ev_attack add_ev_defense add_ev_speed add_ev_special_attack
        self.function_flags_1: int  # add_ev_special_defense add_ev_above_100 add_friendship_1 add_friendship_2 add_friendship_3 unused_1 unused_2 unused_3

        self.ev_hp: int
        self.ev_attack: int
        self.ev_defense: int
        self.ev_speed: int
        self.ev_special_attack: int
        self.ev_special_defense: int

        self.heal_amount: int  # 0 = none, 253 = quarter, 254 = half, 255 = full, otherwise raw hps
        self.pp_gain: int

        self.friendship_1: int
        self.friendship_2: int
        self.friendship_3: int

    @property
    def buy_price(self) -> int:
        return self._price

    @property
    def sell_price(self) -> int:
        return self._price // 2

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
    def cure_inflict_sleep(self) -> bool:
        return bool((self.cure_inflict >> 0) & 0x1)

    @property
    def cure_inflict_poison(self) -> bool:
        return bool((self.cure_inflict >> 1) & 0x1)

    @property
    def cure_inflict_burn(self) -> bool:
        return bool((self.cure_inflict >> 2) & 0x1)

    @property
    def cure_inflict_freeze(self) -> bool:
        return bool((self.cure_inflict >> 3) & 0x1)

    @property
    def cure_inflict_paralysis(self) -> bool:
        return bool((self.cure_inflict >> 4) & 0x1)

    @property
    def cure_inflict_confusion(self) -> bool:
        return bool((self.cure_inflict >> 5) & 0x1)

    @property
    def cure_inflict_infatuation(self) -> bool:
        return bool((self.cure_inflict >> 6) & 0x1)

    @property
    def cure_inflict_guard_spec(self) -> bool:
        return bool((self.cure_inflict >> 7) & 0x1)

    @property
    def revive(self) -> bool:
        return bool((self._boost_0 >> 0) & 0x1)

    @property
    def revive_all(self) -> bool:
        return bool((self._boost_0 >> 1) & 0x1)

    @property
    def rare_exp_candy(self) -> bool:
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

    def category_id(self, identifier: str) -> int:
        return 0
