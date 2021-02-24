from __future__ import annotations

from os.path import join

from utils import fbs_read_as_bool, fbs_read_as_int, fbs_table

from .move_info import MoveInfo


class MoveInfoSwSh(MoveInfo):
    _SIZE = None
    _MAX_MOVE_ID = 826
    _PATH = join("bin", "pml", "waza", "waza{move_id:0>4}.wazabin")

    def __init__(self, table, path: str, item_id: int, data: bytes) -> None:
        super().__init__(table, path, item_id, data)

        self._tab = fbs_table(self._data)

        self.version = fbs_read_as_int(4, self._tab, 4)

        self.move_id = fbs_read_as_int(4, self._tab, 6)
        self.can_use_move = fbs_read_as_bool(self._tab, 8)
        self._type = fbs_read_as_int(1, self._tab, 10)
        self.quality = fbs_read_as_int(1, self._tab, 12)
        self.category = fbs_read_as_int(1, self._tab, 14)
        self._power = fbs_read_as_int(1, self._tab, 16)
        self._accuracy = fbs_read_as_int(1, self._tab, 18)
        self.pp = fbs_read_as_int(1, self._tab, 20)
        self.priority = fbs_read_as_int(1, self._tab, 22, True)
        self.hit_max = fbs_read_as_int(1, self._tab, 24)
        self.hit_min = fbs_read_as_int(1, self._tab, 26)
        self.inflict = fbs_read_as_int(2, self._tab, 28)
        self.inflict_percent = fbs_read_as_int(1, self._tab, 30)
        self.inflict_count = fbs_read_as_int(1, self._tab, 32)
        self.turn_min = fbs_read_as_int(1, self._tab, 34)
        self.turn_max = fbs_read_as_int(1, self._tab, 36)
        self.crit_stage = fbs_read_as_int(1, self._tab, 38)
        self.flinch = fbs_read_as_int(1, self._tab, 40)
        self.effect_sequence = fbs_read_as_int(2, self._tab, 42)
        self.recoil = fbs_read_as_int(1, self._tab, 44, True)
        self.healing = fbs_read_as_int(1, self._tab, 46, True)
        self.target = fbs_read_as_int(1, self._tab, 48)
        self._stat_1 = fbs_read_as_int(1, self._tab, 50)
        self._stat_2 = fbs_read_as_int(1, self._tab, 52)
        self._stat_3 = fbs_read_as_int(1, self._tab, 54)
        self.stat_1_stage = fbs_read_as_int(1, self._tab, 56, True)
        self.stat_2_stage = fbs_read_as_int(1, self._tab, 58, True)
        self.stat_3_stage = fbs_read_as_int(1, self._tab, 60, True)
        self.stat_1_percent = fbs_read_as_int(1, self._tab, 62)
        self.stat_2_percent = fbs_read_as_int(1, self._tab, 64)
        self.stat_3_percent = fbs_read_as_int(1, self._tab, 66)

        self.gigantamax_power = fbs_read_as_int(1, self._tab, 68)

    @property
    def makes_contact(self) -> bool:
        return fbs_read_as_bool(self._tab, 70)

    @property
    def charge(self) -> bool:
        return fbs_read_as_bool(self._tab, 72)

    @property
    def recharge(self) -> bool:
        return fbs_read_as_bool(self._tab, 74)

    @property
    def protect(self) -> bool:
        return fbs_read_as_bool(self._tab, 76)

    @property
    def reflectable(self) -> bool:
        return fbs_read_as_bool(self._tab, 78)

    @property
    def snatch(self) -> bool:
        return fbs_read_as_bool(self._tab, 80)

    @property
    def mirror(self) -> bool:
        return fbs_read_as_bool(self._tab, 82)

    @property
    def punch(self) -> bool:
        return fbs_read_as_bool(self._tab, 84)

    @property
    def sound(self) -> bool:
        return fbs_read_as_bool(self._tab, 86)

    @property
    def gravity(self) -> bool:
        return fbs_read_as_bool(self._tab, 88)

    @property
    def defrost(self) -> bool:
        return fbs_read_as_bool(self._tab, 90)

    @property
    def distance_triple(self) -> bool:
        return fbs_read_as_bool(self._tab, 92)

    @property
    def heal(self) -> bool:
        return fbs_read_as_bool(self._tab, 94)

    @property
    def ignore_substitute(self) -> bool:
        return fbs_read_as_bool(self._tab, 96)

    @property
    def fail_sky_battle(self) -> bool:
        return fbs_read_as_bool(self._tab, 98)

    @property
    def animate_ally(self) -> bool:
        return fbs_read_as_bool(self._tab, 100)

    @property
    def dance(self) -> bool:
        return fbs_read_as_bool(self._tab, 102)

    @property
    def metronome(self) -> bool:
        return fbs_read_as_bool(self._tab, 104)
