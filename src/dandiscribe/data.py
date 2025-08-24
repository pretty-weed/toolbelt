from dataclasses import dataclass
from functools import partial
from typing import Iterator

import scribus

from dandiscribe.enums import COLORS

frozen_dataclass = partial(dataclass, frozen=True, kw_only=True)


COLOR_VALUES = {
    COLORS.LIGHT_BLUE: (64, 18, 0, 2),
    COLORS.PINK: (0, 31, 25, 4),
    COLORS.WHITE: (0, 0, 0, 0),
}
GREY_VAL = (
    sum(COLOR_VALUES[COLORS.LIGHT_BLUE]) // 4 + sum(COLOR_VALUES[COLORS.PINK])
) // 2
COLOR_VALUES[COLORS.GREY] = (GREY_VAL, GREY_VAL, GREY_VAL, GREY_VAL)

for color, values in COLOR_VALUES.items():
    if color in scribus.getColorNames():
        scribus.changeColorCMYK(color, *values)
    else:
        scribus.defineColorCMYK(color, *values)


class NonNegInt(int):
    @classmethod
    def __new__(cls, val):
        if val < 0:
            raise ValueError("Negative values not allowed")
        super().__new__(val)


@frozen_dataclass
class LineStyle:
    weight: NonNegInt
    style: int


@dataclass(frozen=True)
class Margins:
    top: NonNegInt
    right: NonNegInt
    bottom: NonNegInt
    left: NonNegInt

    def __iter__(self) -> Iterator[int]:
        yield from [self.top, self.left, self.bottom, self.right]


@dataclass(frozen=True)
class Size:
    width: NonNegInt
    height: NonNegInt

    @classmethod
    def factory(cls, *in_vals):
        if len(in_vals) == 1:
            return cls(in_vals[0], in_vals[0])
        return cls(*in_vals)

    def __iter__(self) -> Iterator[int]:
        yield from [self.width, self.height]
