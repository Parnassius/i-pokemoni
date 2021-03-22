from __future__ import annotations

from typing import BinaryIO

from utils import read_as_int


class LargeContainer:
    def get_file(self, index: int, sub_file: int = 0) -> bytes:
        return self.get_entry(index, sub_file)

    def _get_file_offset(self, index: int, sub_file: int = 0) -> int:
        raise NotImplementedError

    def get_entry(self, index: int, sub_file: int) -> bytes:
        raise NotImplementedError


class LargeContainerEntry:
    start: int
    end: int
    length: int
    parent_data_position: int

    def get_file_data(self, parent_data: bytes) -> bytes:
        start = self.start + self.parent_data_position
        end = start + self.length
        return parent_data[start:end]
