from __future__ import annotations

import re
import struct
import unicodedata
from typing import BinaryIO

import flatbuffers  # type: ignore


def adjust_stat_id(stat_id: int | str) -> int:
    if isinstance(stat_id, str):
        stat_id = int(stat_id)
    if stat_id == 4:
        stat_id = 6
    elif stat_id in (5, 6):
        stat_id -= 1
    return stat_id


def get_flag(data: bytes, offset: int, bit_index: int) -> bool:
    bit_index &= 7  # ensure bit access is 0-7
    return (data[offset] >> bit_index & 1) != 0


def read_as_int(
    size: int, data: bytes | BinaryIO, offset: int = 0, signed: bool = False
) -> int:
    format_ = {1: "B", 2: "H", 4: "I", 8: "Q"}[size]
    if signed:
        format_ = format_.lower()
    if not isinstance(data, (bytes, bytearray)):
        data = data.read(size)
    return int(struct.unpack_from("<" + format_, data, offset)[0])


def fbs_read_as_int(
    size: int, data: flatbuffers.table.Table, offset: int = 0, signed: bool = False
) -> int:
    if isinstance(size, int):
        format_ = {
            1: [
                flatbuffers.number_types.Uint8Flags,
                flatbuffers.number_types.Int8Flags,
            ],
            2: [
                flatbuffers.number_types.Uint16Flags,
                flatbuffers.number_types.Int16Flags,
            ],
            4: [
                flatbuffers.number_types.Uint32Flags,
                flatbuffers.number_types.Int32Flags,
            ],
            8: [
                flatbuffers.number_types.Uint64Flags,
                flatbuffers.number_types.Int64Flags,
            ],
        }[size][int(signed)]
    else:
        format_ = size
    o = flatbuffers.number_types.UOffsetTFlags.py_type(data.Offset(offset))
    if o != 0:
        return data.Get(format_, o + data.Pos)
    return 0


def fbs_read_as_bool(data: bytes, offset: int = 0) -> bool:
    return bool(fbs_read_as_int(flatbuffers.number_types.BoolFlags, data, offset))


def fbs_table(data: bytes) -> flatbuffers.table.Table:
    pos = flatbuffers.encode.Get(flatbuffers.packer.uoffset, data, 0)
    return flatbuffers.table.Table(data, pos)


def to_id(text: str) -> str:
    text = "".join(
        [c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)]
    )
    text = text.lower()
    text = text.replace("★", "dynamax-crystal-")
    text = text.replace("♀", "-f")
    text = text.replace("♂", "-m")
    text = re.sub(r"[\.’]+", "", text)
    text = re.sub(r"[\s:,]+", "-", text)
    return text.strip("-")
