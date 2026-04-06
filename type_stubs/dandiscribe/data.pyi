from dandiscribe.enums import HAlign as HAlign, Unit as Unit, VAlign as VAlign
from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import (
    Coord as Coord,
    Rect as _Rect,
    Size as _Size,
)
from dataclasses import dataclass
from functools import lru_cache
from typing import NamedTuple, Self

@dataclass
class Align:
    vertical: VAlign = ...
    horizontal: HAlign = ...

class Rect(MixableNamedTuple, _Rect):
    def create(self, offset: Coord = ..., name: str = "") -> str: ...

class Size(MixableNamedTuple, _Size):
    unit: Unit
    def as_points(self) -> Self: ...
    def as_unit(self, unit: Unit) -> Self: ...

class Margins(NamedTuple):
    top: float
    right: float
    bottom: float
    left: float
    @lru_cache
    def as_tuple(self) -> tuple[float, float, float, float]: ...
    @property
    @lru_cache
    def horizontal(self) -> float: ...
    @property
    @lru_cache
    def vertical(self) -> float: ...
    def with_top(self, top_val: int): ...
    def with_right(self, right_val: int): ...
    def with_bottom(self, bottom_val: int): ...
    def with_left(self, left_val: int): ...
