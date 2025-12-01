from _typeshed import Incomplete
from dandiscribe.enums import HAlign as HAlign, VAlign as VAlign
from dataclasses import dataclass
from enum import Enum as Enum
from functools import cache as cache, partial as partial
from typing import NamedTuple

@dataclass
class Align:
    vertical: VAlign = ...
    horizontal: HAlign = ...

class _Margins(NamedTuple):
    top: Incomplete
    right: Incomplete
    bottom: Incomplete
    left: Incomplete

class Margins(_Margins):
    def with_top(self, top_val: int): ...
    def with_right(self, right_val: int): ...
    def with_bottom(self, bottom_val: int): ...
    def with_left(self, left_val: int): ...
