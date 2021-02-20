from __future__ import annotations

from os.path import join
from typing import NamedTuple

from utils import read_as_int


class TextLine(NamedTuple):
    offset: int
    length: int


class TextFile:
    _PATHS = {
        "letsgo": ["bin", "message", None, "common"],
        "swsh": ["bin", "message", None, "common"],
    }

    _KEY_TBLMAGIC = 0x42544841

    _KEY_BASE = 0x7C89
    _KEY_ADVANCE = 0x2983
    _KEY_VARIABLE = 0x0010
    _KEY_TERMINATOR = 0x0000
    _KEY_TEXTRETURN = 0xBE00
    _KEY_TEXTCLEAR = 0xBE01
    _KEY_TEXTWAIT = 0xBE02
    _KEY_TEXTNULL = 0xBDFF

    def __init__(
        self, path: str, language: str, filename: str, file_format: str
    ) -> None:
        self._filename = filename
        self._format = file_format

        path = join(path, *[i if i else language for i in self._PATHS[self._format]])
        with open(join(path, filename + ".tbl"), "rb") as f:
            self._labels = f.read()
        with open(join(path, filename + ".dat"), "rb") as f:
            self._data = f.read()

        if self._labels_magic != self._KEY_TBLMAGIC:
            raise Exception("Invalid tbl magic")

        if self._initial_key != 0:
            raise Exception("Invalid initial key! Not 0?")
        if (
            self._section_data_offset + self._total_length != len(self._data)
            or self._text_sections != 1
        ):
            raise Exception("Invalid Text File")
        if self._section_length != self._total_length:
            raise Exception("Section size and overall size do not match")

    @property
    def _labels_magic(self) -> int:
        return read_as_int(4, self._labels, 0x0)

    @property
    def _labels_line_count(self) -> int:
        return read_as_int(4, self._labels, 0x4)

    @property
    def _parsed_labels(self) -> list[str]:
        offset = 0x8
        result = []
        for _ in range(0, self._labels_line_count):
            # label_hash = read_as_int(8, self._labels, offset)
            offset += 0x8
            name_length = read_as_int(2, self._labels, offset)
            offset += 0x2
            name = self._labels[offset : offset + name_length - 1].decode()
            offset += name_length

            if name != "msg_" + self._filename + "_max":
                result.append(name)

        return result

    @property
    def _text_sections(self) -> int:
        return read_as_int(2, self._data, 0x0)  # Always 0x0001

    @property
    def _line_count(self) -> int:
        return read_as_int(2, self._data, 0x2)

    @property
    def _total_length(self) -> int:
        return read_as_int(4, self._data, 0x4)

    @property
    def _initial_key(self) -> int:
        return read_as_int(4, self._data, 0x8)  # Always 0x00000000

    @property
    def _section_data_offset(self) -> int:
        return read_as_int(4, self._data, 0xC)  # Always 0x0010

    @property
    def _section_length(self) -> int:
        return read_as_int(4, self._data, self._section_data_offset)

    @property
    def _line_offsets(self) -> list[TextLine]:
        result: list[TextLine] = []
        sdo = self._section_data_offset
        for i in range(self._line_count):
            result.append(
                TextLine(
                    read_as_int(4, self._data, (i * 8) + sdo + 4) + sdo,  # offset
                    read_as_int(2, self._data, (i * 8) + sdo + 8),  # length
                )
            )
        return result

    def _get_line_string(self, data: bytes) -> str:
        char_map = {
            0xE07F: 0x202F,  # nbsp
            0xE08D: 0x2026,  # …
            0xE08E: 0x2642,  # ♂
            0xE08F: 0x2640,  # ♀
        }

        s = ""
        i = 0
        while i < len(data):
            val = read_as_int(2, data, i)
            i += 2

            if val == self._KEY_TERMINATOR:
                break

            if val == self._KEY_VARIABLE:
                i, s = self._get_variable_string(data, i, s)
            else:
                s += chr(char_map.get(val, val))
        return s

    def _get_variable_string(self, data: bytes, i: int, s: str) -> tuple[int, str]:
        count = read_as_int(2, data, i)
        i += 2
        variable = read_as_int(2, data, i)
        i += 2

        if variable == self._KEY_TEXTRETURN:
            # "Waitbutton then scroll text \r"
            s += "\\r"
        elif variable == self._KEY_TEXTCLEAR:
            # "Waitbutton then clear text \c"
            s += "\\c"
        elif variable == self._KEY_TEXTWAIT:
            # Dramatic pause for a text line. New!
            time = read_as_int(2, data, i)
            i += 2
            s += f"[WAIT {time}]"
        elif variable == self._KEY_TEXTNULL:
            # Empty Text line?
            # Includes linenum so maybe for betatest finding used-unused lines?
            line = read_as_int(2, data, i)
            i += 2
            s += f"[~ {line}]"
        else:
            # string varName = config.GetVariableString(variable);
            var = ""
            var_args = []
            if count > 1:
                for _ in range(1, count):
                    arg = read_as_int(2, data, i)
                    i += 2
                    var_args.append(f"{arg:0>4X}")
            if var_args:
                var += "(" + (",".join(var_args)) + ")"
            s += f"[VAR {var}]"

        return i, s

    @property
    def _parsed_data(self) -> list[str]:
        key = self._KEY_BASE
        result = []
        lines = self._line_offsets
        for line in lines:
            start = line.offset
            end = start + line.length * 2
            line_data = bytearray(self._data[start:end])

            key0 = key
            for i in range(0, len(line_data), 2):
                line_data[i] ^= key0 % 2 ** 8
                line_data[i + 1] ^= (key0 >> 8) % 2 ** 8
                key0 = (key0 << 3 | key0 >> 13) % 2 ** 16

            result.append(self._get_line_string(line_data))
            key = (key + self._KEY_ADVANCE) % 2 ** 16

        return result

    @property
    def lines(self) -> list[tuple[str, str]]:
        labels = self._parsed_labels
        data = self._parsed_data
        if len(labels) != len(data):
            raise Exception("tbl and dat line counts do not match")
        return list(zip(labels, data))
