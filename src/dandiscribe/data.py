from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from turtle import heading
from typing import Any, Literal, NamedTuple, Self, override

from dandy_lib.datatypes.tuples import MixableNamedTuple
import scribus

from dandy_lib.datatypes.numeric import NonNegNum
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
