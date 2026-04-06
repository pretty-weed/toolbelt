import datetime
from enum import auto, unique, Enum, IntEnum, StrEnum
from typing import NamedTuple, override

from icalendar import prop
import scribus


class COLORS(StrEnum):
    NONE = "None"
    LIGHT_BLUE = "light_blue"
    PINK = "pink"
    WHITE = "white"
    GREY = "grey"
    BLACK = "Black"
    WARM_BLACK = "Warm Black"
    COOL_BLACK = "Cool Black"
    RICH_BLACK = "Rich Black"


class FILL(StrEnum):
    DOTS = "dots"
    CLEAR = "clear"


class PAGESIDE(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    EITHER = "either"


@unique
class VAlign(IntEnum):
    TOP = scribus.ALIGNV_TOP
    CENTERED = scribus.ALIGNV_CENTERED
    BOTTOM = scribus.ALIGNV_BOTTOM
    JUSTIFIED = auto()


@unique
class HAlign(IntEnum):
    LEFT = scribus.ALIGN_LEFT
    CENTERED = scribus.ALIGN_CENTERED
    RIGHT = scribus.ALIGN_RIGHT
    FORCED_JUSTIFY = scribus.ALIGN_FORCED
    JUSTIFY = scribus.ALIGN_BLOCK


@unique
class FontFeature(StrEnum):
    INHERIT = "inherit"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    UNDERLINEWORDS = "underlinewords"
    STRIKE = "strike"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"
    OUTLINE = "outline"
    SHADOWED = "shadowed"
    ALLCAPS = "allcaps"
    SMALLCAPS = "smallcaps"


class FontFaces(StrEnum):
    CHANCERY_MED = "QTChanceryType Medium"
    CHANCERY_BOLD = "QTChanceryType Bold"
    CHANCERY_ITALIC = "QTChanceryType Italic"
    FRAKTUR = "Des Malers Fraktur Regular"


class LinespacingMode(IntEnum):
    FIXED = 0
    AUTOMATIC = 1
    BASELINE_GRID = 2


class _Unit(NamedTuple):
    name: str
    aliases: list[str]
    pt_multiplier: float
    const_enum: int

    @override
    def __eq__(self, value: object, /) -> bool:
        return (
            value is self
            or value == self.const_enum
            or value == self.name
            or value in self.aliases
        )


class Unit(Enum):
    CENTIMETERS = _Unit("CENTIMETERS", ["CM"], scribus.cm, scribus.UNIT_CM)
    CICERO = _Unit("CICERO", [], scribus.c, scribus.UNIT_CICERO)
    INCHES = _Unit("INCHES", ["IN", "INCH"], scribus.inch, scribus.UNIT_INCHES)
    MILLIMETERS = _Unit("MILLIMETERS", ["MM"], scribus.mm, scribus.UNIT_MM)
    PICAS = _Unit("PICAS", ["P", "PICA"], scribus.p, scribus.UNIT_PICAS)
    POINTS = _Unit("POINTS", ["PT", "POINT"], scribus.pt, scribus.UNIT_PT)

    @property
    def pt_multiplier(self) -> float:
        return self.value.pt_multiplier

    @property
    def const_enum(self) -> int:
        return self.value.const_enum

    @property
    def aliases(self) -> list[str]:
        return self.value.aliases

    @classmethod
    def get(cls, key: str | int) -> _Unit:
        return cls.get_item(key)[1]

    @classmethod
    def get_item(cls, key: str | int) -> tuple[str, _Unit]:
        for u in cls:
            if u.value == key:
                return u.name, u.value
        raise KeyError(f"{key} not found!")

    def __matmul__(self, other: "Unit | _Unit") -> float:
        print(f"{self} @ {other}")
        return other.pt_multiplier / self.pt_multiplier

    def __rmatmul__(self, other: "Unit | _Unit") -> float:
        return self.__matmul__(other)
