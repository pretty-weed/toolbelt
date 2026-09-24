from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal, NamedTuple, Self, override

import scribus
from dandy_lib.datatypes.numeric import NonNegNum
from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import (
    ZERO_COORD,
    Coord,
)
from dandy_lib.datatypes.twodee import (
    Rect as _Rect,
)
from dandy_lib.datatypes.twodee import (
    Size as _Size,
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
            scribus.pointsToDocUnit(self.size.as_points().width),
            scribus.pointsToDocUnit(self.size.as_points().height),
            *name_arg,
        )

    @override
    def __str__(self) -> str:
        conv_part = ""
        if self.unit is not Unit.INCHES:
            conv_part = f' ({self.width * (self.unit @ Unit.INCHES)}", {self.height * (self.unit@Unit.INCHES)})"'
        return f"Rect(position=Coord(x={self.x}, y={self.y}), size=Size(width={self.width}, height={self.height}){conv_part}, unit={self.unit.name})"


class Size(MixableNamedTuple, _Size):
    unit: Unit = Unit.POINTS

    @override
    @classmethod
    def factory(cls, *in_vals: NonNegNum, unit: Unit = Unit.POINTS) -> Self:
        if len(in_vals) == 1:
            in_vals *= 2
        return cls(*in_vals, unit)

    def as_points(self) -> Self:
        return self.as_unit(Unit.POINTS)

    def for_scribus(self, unit=None) -> tuple[float, float]:
        if unit is None or unit is self.unit:
            return (self.width, self.height)
        conversion_factor: float = self.unit @ unit
        return (self.width * conversion_factor, self.height * conversion_factor)

    def as_unit(self, unit: Unit) -> Self:
        multiplier: float = self.unit @ unit
        return self.__class__(
            self.width * multiplier, self.height * multiplier, unit
        )

    def __len__(self) -> Literal[2]:
        return 2

    def __iter__(self) -> Iterable[NonNegNum]:
        yield self.width
        yield self.height


assert len(list(Size(1, 3))) == 2


class _NotSet(float):
    def __new__(cls, value=-float("inf")):
        if value > -float("inf"):
            raise ValueError("what you doing with not set?")
        return super().__new__(cls, -float("inf"))


NOT_SET = _NotSet()


class Margins(NamedTuple):
    left: float = NOT_SET
    right: float = NOT_SET
    top: float = NOT_SET
    bottom: float = NOT_SET
    facing: bool = False

    @property
    def inside(self) -> float:
        if not self.facing:
            raise TypeError("Non-facing margins do not have inside or outside")
        return self.left

    @property
    def outside(self) -> float:
        if not self.facing:
            raise TypeError("Non-facing margins do not have inside our outside")
        return self.right

    @lru_cache
    def as_tuple(self) -> tuple[float, float, float, float]:
        return tuple[float, float, float, float](self)

    @property
    def horizontal(self) -> float:
        return self.right + self.left

    @property
    def vertical(self) -> float:
        return self.top + self.bottom

    def with_top(self, top_val: float) -> Self:
        return self.__class__(top_val, self.right, self.bottom, self.left)

    def with_right(self, right_val: float) -> Self:
        return self.__class__(self.top, right_val, self.bottom, self.left)

    def with_bottom(self, bottom_val: float) -> Self:
        return self.__class__(self.top, self.right, bottom_val, self.left)

    def with_left(self, left_val: float) -> Self:
        return self.__class__(self.top, self.right, self.bottom, left_val)
