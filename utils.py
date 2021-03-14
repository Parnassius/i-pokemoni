from __future__ import annotations

import re
import struct
import unicodedata
from collections.abc import Callable
from typing import Protocol

import flatbuffers  # type: ignore


def get_flag(data: bytes, offset: int, bit_index: int) -> bool:
    bit_index &= 7  # ensure bit access is 0-7
    return (data[offset] >> bit_index & 1) != 0


def read_as_int(size: int, data: bytes, offset: int = 0, signed: bool = False) -> int:
    format_ = {1: "B", 2: "H", 4: "I", 8: "Q"}[size]
    if signed:
        format_ = format_.lower()
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


def fbs_read_as_bool(data: flatbuffers.table.Table, offset: int = 0) -> bool:
    return bool(fbs_read_as_int(flatbuffers.number_types.BoolFlags, data, offset))


class T(Protocol):
    def __init__(self, data: bytes, pos: int) -> None:
        ...


def fbs_read_as_vector(
    vector: type[T], size: int, data: flatbuffers.table.Table, offset: int = 0
) -> list[T]:
    o = flatbuffers.number_types.UOffsetTFlags.py_type(data.Offset(offset))
    if o != 0:
        items = []
        for j in range(data.VectorLen(o)):
            x = data.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * size
            x = data.Indirect(x)

            items.append(vector(data.Bytes, x))
        return items
    return []


def fbs_table(data: bytes, pos: int | None = None) -> flatbuffers.table.Table:
    if pos is None:
        pos = flatbuffers.encode.Get(flatbuffers.packer.uoffset, data, 0)
    return flatbuffers.table.Table(data, pos)


def hash_fnv1a_64(data: str) -> int:
    k_fnv_prime_64 = 0x00000100000001B3
    k_offset_basis_64 = 0xCBF29CE484222645

    hash_ = k_offset_basis_64
    for i in data:
        hash_ ^= ord(i)
        hash_ *= k_fnv_prime_64

    return hash_ & 0xFFFFFFFFFFFFFFFF


def to_id(*text: str, separator: str = "--") -> str:
    result = []
    for t in text:
        t = "".join(
            [
                c
                for c in unicodedata.normalize("NFKD", t)
                if not unicodedata.combining(c)
            ]
        )
        t = t.lower()
        t = t.replace("★", "dynamax-crystal-")
        t = t.replace("♀", "-f")
        t = t.replace("♂", "-m")
        t = re.sub(r"[\.’]+", "", t)
        t = re.sub(r"[\s:,]+", "-", t)
        t = t.strip("-")
        if t:
            result.append(t)
    return "--".join(result)
