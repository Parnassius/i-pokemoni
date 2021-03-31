from __future__ import annotations

from os.path import join

from utils import read_as_int

from .move_info import MoveInfo


class MoveInfoSM(MoveInfo):
    _SIZE = 0x28
    _TYPE = "garc_mini"
    _PATH = join("a", "0", "1", "1")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._type = int(self._data[0x00])
        self.quality = int(self._data[0x01])
        self.category = int(self._data[0x02])
        self._power = int(self._data[0x03])
        self._accuracy = int(self._data[0x04])
        self.pp = int(self._data[0x05])
        self.priority = read_as_int(1, self._data, 0x06, True)
        self.hit_min = int(self._data[0x07] & 0x0F)
        self.hit_max = int(self._data[0x07] >> 4)
        self.inflict = read_as_int(2, self._data, 0x08)
        self.inflict_percent = int(self._data[0x0A])
        self.inflict_count = int(self._data[0x0B])
        self.turn_min = int(self._data[0x0C])
        self.turn_max = int(self._data[0x0D])
        self.crit_stage = int(self._data[0x0E])
        self.flinch = int(self._data[0x0F])
        self.effect_sequence = read_as_int(2, self._data, 0x10)
        self.recoil = read_as_int(1, self._data, 0x12, True)
        self.healing = read_as_int(1, self._data, 0x13, True)
        self.target = int(self._data[0x14])
        self._stat_1 = int(self._data[0x15])
        self._stat_2 = int(self._data[0x16])
        self._stat_3 = int(self._data[0x17])
        self.stat_1_stage = read_as_int(1, self._data, 0x18, True)
        self.stat_2_stage = read_as_int(1, self._data, 0x19, True)
        self.stat_3_stage = read_as_int(1, self._data, 0x1A, True)
        self.stat_1_percent = int(self._data[0x1B])
        self.stat_2_percent = int(self._data[0x1C])
        self.stat_3_percent = int(self._data[0x1D])

        self.z_move = read_as_int(2, self._data, 0x1E)
        self.z_power = int(self._data[0x20])
        self.z_effect = int(
            self._data[0x21]
        )  # https://github.com/kwsch/pk3DS/blob/754b9b8d95ada3a67989c42e5713ad90060d343f/pk3DS/Subforms/Gen7/MoveEditor7.cs#L54:L87

        self.refresh_afflict_type = int(
            self._data[0x22]
        )  # https://github.com/kwsch/pkNX/blob/2c990d2b7dc2189f524417e741d46fc763f194d9/pkNX.Structures/Move/RefreshType.cs
        self.refresh_afflict_percent = int(self._data[0x23])

        self._flags = read_as_int(4, self._data, 0x24)
