import re
import struct
import unicodedata


def get_flag(data: bytes, offset: int, bit_index: int) -> bool:
    bit_index &= 7  # ensure bit access is 0-7
    return (data[offset] >> bit_index & 1) != 0


def read_as_int(size: int, data: bytes, offset: int = 0, signed: bool = False) -> int:
    format = {1: "B", 2: "H", 4: "I", 8: "Q"}[size]
    if signed:
        format = format.lower()
    return int(struct.unpack_from("<" + format, data, offset)[0])


def to_id(text: str) -> str:
    text = "".join(
        [c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)]
    )
    text = text.lower()
    text = text.replace("♀", "-f")
    text = text.replace("♂", "-m")
    text = re.sub(r"[\.’]+", "", text)
    text = re.sub(r"[\s:]+", "-", text)
    return text.strip("-")
