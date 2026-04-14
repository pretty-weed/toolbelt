import logging
from dandiscribe.log import configure as configure
from dandy_lib.cli.enums import ChoiceEnumMeta, ChoiceEnumMixin
from dandy_lib.datatypes.twodee import Number as Number
from enum import Enum, IntEnum, StrEnum
from multiprocessing import Value as Value
from typing import ClassVar, Self, override

LOGGER: logging.Logger

class PaperSize(
    ChoiceEnumMixin, tuple[float, float], Enum, metaclass=ChoiceEnumMeta
):
    LETTER = ...
    LEGAL = ...
    A5 = ...
    A4 = ...
    LETTER_HALF = ...

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

class UnitType:
    __instances__: ClassVar[dict[str, Self]]
    unit: str
    aliases: list[str]
    pt_multiplier: float
    const_enum: int
    def __new__(
        cls,
        unit: str,
        aliases: list[str],
        pt_multiplier: float,
        const_enum: int,
    ) -> Self: ...
    def __init__(
        self,
        unit: str,
        aliases: list[str],
        pt_multiplier: float,
        const_enum: int,
    ) -> None: ...

class Unit(ChoiceEnumMixin, UnitType, Enum, metaclass=ChoiceEnumMeta):
    CENTIMETERS = ...
    CICERO = ...
    INCHES = ...
    MILLIMETERS = ...
    PICAS = ...
    POINTS = ...
    def __hash__(self): ...
    def __new__(
        cls,
        name: str,
        aliases: list[str],
        pt_multiplier: float,
        const_enum: int,
    ) -> Self: ...
    @property
    def in_to_pt(self) -> float: ...
    @classmethod
    def get_current(cls) -> Self: ...
    @classmethod
    def get(cls, key: str | int) -> Self: ...
    @classmethod
    def get_val(cls, key: str | int) -> UnitType: ...
    @classmethod
    def get_item(cls, key: str | int) -> tuple[str, UnitType]: ...
    def __int__(self) -> int: ...
    @override
    def __eq__(self, value: object) -> bool: ...
    def __matmul__(self, other: Unit | UnitType) -> float: ...
    def __rmatmul__(self, other: Unit | UnitType) -> float: ...
    def __mul__(self, other: Number) -> float: ...
    def __rmul__(self, other: Number) -> float: ...
