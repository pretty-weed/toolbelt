from dataclasses import dataclass
from functools import lru_cache
from typing import Iterator, NamedTuple, Union

import scribus

from dandiscribe.enums import HAlign, VAlign


@dataclass
class Align:
    vertical: VAlign = VAlign.TOP
    horizontal: HAlign = HAlign.LEFT


class Margins(NamedTuple):
    top: float
    right: float
    bottom: float
    left: float

    @property
    @lru_cache
    def horizontal(self) -> float:
        return self.right + self.left

    @property
    @lru_cache
    def vertical(self) -> float:
        return self.top + self.bottom

    def with_top(self, top_val: int):
        return self.__class__(top_val, self.right, self.bottom, self.left)

    def with_right(self, right_val: int):
        return self.__class__(self.top, right_val, self.bottom, self.left)

    def with_bottom(self, bottom_val: int):
        return self.__class__(self.top, self.right, bottom_val, self.left)

    def with_left(self, left_val: int):
        return self.__class__(self.top, self.right, self.bottom, left_val)
