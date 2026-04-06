from enum import Enum, IntEnum, StrEnum
from icalendar import prop as prop
from typing import NamedTuple, override

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

class VAlign(IntEnum):
    TOP = ...
    CENTERED = ...
    BOTTOM = ...
    JUSTIFIED = ...

class HAlign(IntEnum):
    LEFT = ...
    CENTERED = ...
    RIGHT = ...
    FORCED_JUSTIFY = ...
    JUSTIFY = ...

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
    def __eq__(self, value: object) -> bool: ...

class Unit(Enum):
    CENTIMETERS = ...
    CICERO = ...
    INCHES = ...
    MILLIMETERS = ...
    PICAS = ...
    POINTS = ...
    @property
    def pt_multiplier(self) -> float: ...
    @property
    def const_enum(self) -> int: ...
    @property
    def aliases(self) -> list[str]: ...
    @classmethod
    def get(cls, key: str | int) -> _Unit: ...
    @classmethod
    def get_item(cls, key: str | int) -> tuple[str, _Unit]: ...
    def __matmul__(self, other: Unit | _Unit) -> float: ...
    def __rmatmul__(self, other: Unit | _Unit) -> float: ...
