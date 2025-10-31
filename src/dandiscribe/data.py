from collections import namedtuple
from dataclasses import dataclass
import datetime
from enum import Enum
from functools import cache, partial
from typing import Iterator, Union

import scribus

from dandiscribe.enums import HAlign, VAlign

@dataclass
class Align:
    vertical: VAlign = VAlign.TOP
    horizontal: HAlign = HAlign.LEFT

_Margins = namedtuple("Margins", ["top", "right", "bottom", "left"])
class Margins(_Margins):

    def with_top(self, top_val: int):
        return self.__class__(top_val, self.right, self.bottom, self.left)
    def with_right(self, right_val: int):
        return self.__class__(self.top, right_val, self.bottom, self.left)
    def with_bottom(self, bottom_val: int):
        return self.__class__(self.top, self.right, bottom_val, self.left)
    def with_left(self, left_val: int):
        return self.__class__(self.top, self.right, self.bottom, left_val)

