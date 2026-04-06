from dataclasses import dataclass
from functools import lru_cache
from typing import NamedTuple, Self

from dandy_lib.datatypes.tuples import MixableNamedTuple
import scribus

from dandy_lib.datatypes.twodee import (
    Coord,
    Rect as _Rect,
    Size as _Size,
    ZERO_COORD,
)

from dandiscribe.enums import HAlign, Unit, VAlign


@dataclass
class Align:
    vertical: VAlign = VAlign.TOP
    horizontal: HAlign = HAlign.LEFT


class Rect(MixableNamedTuple, _Rect):
    def create(self, offset: Coord = ZERO_COORD, name: str = "") -> str:
        if name:
            name_arg = [
                name,
            ]
        else:
            name_arg = []
        return scribus.createRect(
            self.x + offset.x,
            self.y + offset.y,
            self.width,
            self.height,
            *name_arg,
        )


class Size(MixableNamedTuple, _Size):
    unit: Unit = Unit.POINTS

    def as_points(self) -> Self:
        return self.as_unit(Unit.POINTS)

    def as_unit(self, unit: Unit) -> Self:
        multiplier: float = self.unit @ Unit.POINTS
        return self.__class__(
            self.x * multiplier, self.y * multiplier, Unit.POINTS
        )


class Margins(NamedTuple):
    top: float
    right: float
    bottom: float
    left: float

    @lru_cache
    def as_tuple(self) -> tuple[float, float, float, float]:
        return tuple[float, float, float, float](self)

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
