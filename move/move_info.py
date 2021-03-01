from __future__ import annotations

from base import BaseInfo


class MoveInfo(BaseInfo):
    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._type: int
        self.quality: int
        self.category: int
        self._power: int
        self._accuracy: int
        self.pp: int
        self.priority: int
        self.hit_min: int
        self.hit_max: int
        self.inflict: int
        self.inflict_percent: int
        self.inflict_count: int  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Move/MoveInflictDuration.cs
        self.turn_min: int
        self.turn_max: int
        self.crit_stage: int
        self.flinch: int
        self.effect_sequence: int
        self.recoil: int
        self.healing: int
        self.target: int  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Move/MoveTarget.cs
        self._stat_1: int
        self._stat_2: int
        self._stat_3: int
        self.stat_1_stage: int
        self.stat_2_stage: int
        self.stat_3_stage: int
        self.stat_1_percent: int
        self.stat_2_percent: int
        self.stat_3_percent: int

        self._flags: int

    @property
    def makes_contact(self) -> bool:
        # Makes contact.
        return bool(self._flags >> 0x00 & 1)

    @property
    def charge(self) -> bool:
        # The user is unable to make a move between turns.
        return bool(self._flags >> 0x01 & 1)

    @property
    def recharge(self) -> bool:
        # If this move is successful, the user must recharge on the following turn and cannot make a move.
        return bool(self._flags >> 0x02 & 1)

    @property
    def protect(self) -> bool:
        # Blocked by Detect, Protect, Spiky Shield, and if not a Status move, King's Shield.
        return bool(self._flags >> 0x03 & 1)

    @property
    def reflectable(self) -> bool:
        # Bounced back to the original user by Magic Coat or the Magic Bounce Ability.
        return bool(self._flags >> 0x04 & 1)

    @property
    def snatch(self) -> bool:
        # Can be stolen from the original user and instead used by another Pokemon using Snatch.
        return bool(self._flags >> 0x05 & 1)

    @property
    def mirror(self) -> bool:
        # Can be copied by Mirror Move.
        return bool(self._flags >> 0x06 & 1)

    @property
    def punch(self) -> bool:
        # Power is multiplied when used by a Pokemon with the Iron Fist Ability.
        return bool(self._flags >> 0x07 & 1)

    @property
    def sound(self) -> bool:
        # Has no effect on Pokemon with the Soundproof Ability.
        return bool(self._flags >> 0x08 & 1)

    @property
    def gravity(self) -> bool:
        # Prevented from being executed or selected during Gravity's effect.
        return bool(self._flags >> 0x09 & 1)

    @property
    def defrost(self) -> bool:
        # Thaws the user if executed successfully while the user is frozen.
        return bool(self._flags >> 0x0A & 1)

    @property
    def distance_triple(self) -> bool:
        # Can target a Pokemon positioned anywhere in a Triple Battle.
        return bool(self._flags >> 0x0B & 1)

    @property
    def heal(self) -> bool:
        # Prevented from being executed or selected during Heal Block's effect.
        return bool(self._flags >> 0x0C & 1)

    @property
    def ignore_substitute(self) -> bool:
        # Ignores a target's substitute.
        return bool(self._flags >> 0x0D & 1)

    @property
    def fail_sky_battle(self) -> bool:
        # Prevented from being executed or selected in a Sky Battle.
        return bool(self._flags >> 0x0E & 1)

    @property
    def animate_ally(self) -> bool:
        # Always animate the move when used on an ally.
        return bool(self._flags >> 0x0F & 1)

    @property
    def dance(self) -> bool:
        # When used by a Pokemon, other Pokemon with the Dancer Ability can attempt to execute the same move.
        return bool(self._flags >> 0x10 & 1)

    @property
    def type(self) -> int:
        return self._type + 1

    @property
    def target_id(self) -> int:
        return {
            13: 1,  # specific-move
            3: 2,  # selected-pokemon-me-first
            2: 3,  # ally
            12: 4,  # users-field
            1: 5,  # user-or-ally
            11: 6,  # opponents-field
            7: 7,  # user
            9: 8,  # random-opponent
            4: 9,  # all-other-pokemon
            0: 10,  # selected-pokemon
            5: 11,  # all-opponents
            10: 12,  # entire-field
            6: 13,  # user-and-allies
            8: 14,  # all-pokemon
        }[self.target]

    @property
    def damage_class_id(self) -> int:
        return self.category + 1

    @property
    def power(self) -> int:
        if self._power == 1:
            return 0
        return self._power

    @property
    def accuracy(self) -> int:
        return self._accuracy % 101

    @property
    def effect_id(self) -> int:
        return self.effect_sequence + 1

    @property
    def effect_chance(self) -> int:
        return self.inflict_percent or self.flinch or self.stat_chance

    def flags(self, identifier) -> set[int]:
        result = set()
        if self.makes_contact:
            result.add(1)
        if self.charge:
            result.add(2)
        if self.recharge:
            result.add(3)
        if self.protect:
            result.add(4)
        if self.reflectable:
            result.add(5)
        if self.snatch:
            result.add(6)
        if self.mirror:
            result.add(7)
        if self.punch:
            result.add(8)
        if self.sound:
            result.add(9)
        if self.gravity:
            result.add(10)
        if self.defrost:
            result.add(11)
        if self.distance_triple:
            result.add(12)
        if self.heal:
            result.add(13)
        if self.ignore_substitute:
            result.add(14)
        if identifier in (
            "cotton-spore",
            "magic-powder",
            "poison-powder",
            "powder",
            "rage-powder",
            "sleep-powder",
            "spore",
            "stun-spore",
        ):  # powder
            result.add(15)
        if identifier in (
            "bite",
            "crunch",
            "fire-fang",
            "fishious-rend",
            "hyper-fang",
            "ice-fang",
            "jaw-lock",
            "poison-fang",
            "psychic-fangs",
            "thunder-fang",
        ):  # bite
            result.add(16)
        if identifier in (
            "aura-sphere",
            "dark-pulse",
            "dragon-pulse",
            "heal-pulse",
            "origin-pulse",
            "terrain-pulse",
            "water-pulse",
        ):  # pulse
            result.add(17)  #
        if identifier in (
            "acid-spray",
            "aura-sphere",
            "barrage",
            "beak-blast",
            "bullet-seed",
            "egg-bomb",
            "electro-ball",
            "energy-ball",
            "focus-blast",
            "gyro-ball",
            "ice-ball",
            "magnet-bomb",
            "mist-ball",
            "mud-bomb",
            "octazooka",
            "pollen-puff",
            "pyro-ball",
            "rock-blast",
            "rock-wrecker",
            "searing-shot",
            "seed-bomb",
            "shadow-ball",
            "sludge-bomb",
            "weather-ball",
            "zap-cannon",
        ):  # ballistics
            result.add(18)
        if identifier in (
            "attract",
            "disable",
            "encore",
            "heal-block",
            "taunt",
            "torment",
        ):  # mental
            result.add(19)
        if self.fail_sky_battle:
            result.add(20)
        if self.dance:
            result.add(21)

        return result

    @property
    def stat_chance(self) -> int:
        return self.stat_1_percent or self.stat_2_percent or self.stat_3_percent

    @property
    def meta_category_id(self) -> int:
        return self.quality

    @property
    def meta_ailment_id(self) -> int:
        if self.inflict == 65535:
            return -1
        return self.inflict

    def stat(self, num: int) -> set[int]:
        stat_ = [self._stat_1, self._stat_2, self._stat_3][num]
        if stat_ == 0:
            return set()
        elif stat_ <= 7:
            return {stat_ + 1}
        else:
            return {2, 3, 4, 5, 6}

    def stat_change(self, num: int) -> tuple[set[int], int]:
        return (
            self.stat(num),
            [self.stat_1_stage, self.stat_2_stage, self.stat_3_stage][num],
        )

    @property
    def stat_changes(self) -> set[int]:
        result = set()
        for i in range(3):
            if stat_ := self.stat(i):
                result.update(stat_)
        return result
