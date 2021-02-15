import struct


def get_flag(data: bytes, offset: int, bit_index: int) -> bool:
    bit_index &= 7  # ensure bit access is 0-7
    return (data[offset] >> bit_index & 1) != 0


def read_as_int(size: int, data: bytes, offset: int = 0) -> int:
    formats = {2: "H", 4: "I", 8: "Q"}
    return int(struct.unpack_from("<" + formats[size], data, offset)[0])
