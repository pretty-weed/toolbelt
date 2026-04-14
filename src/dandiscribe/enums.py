import datetime
from enum import auto, unique, Enum, IntEnum, StrEnum
import logging
from multiprocessing import Value
from typing import ClassVar, Self, Tuple, override

from dandy_lib.datatypes.twodee import Number
from dandy_lib.cli.enums import ChoiceEnumMeta, ChoiceEnumMixin
import scribus

from dandiscribe.log import configure


LOGGER: logging.Logger = configure(__name__)


class PaperSize(
    ChoiceEnumMixin, tuple[float, float], Enum, metaclass=ChoiceEnumMeta
):
    LETTER = scribus.PAPER_LETTER
    LEGAL = scribus.PAPER_LEGAL
    A5 = scribus.PAPER_A5
    A4 = scribus.PAPER_A4
    LETTER_HALF = (LETTER[1] / 2.0, LETTER[0])


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


class UnitType:
    __slots__: ClassVar[tuple[str, ...]] = (
        "unit",
        "aliases",
        "pt_multiplier",
        "const_enum",
    )
    __instances__: ClassVar[dict[str, Self]] = {}

    unit: str  # pyright: ignore[reportUninitializedInstanceVariable]
    aliases: list[str]  # pyright: ignore[reportUninitializedInstanceVariable]
    pt_multiplier: float  # pyright: ignore[reportUninitializedInstanceVariable]
    const_enum: int  # pyright: ignore[reportUninitializedInstanceVariable]

    def __new__(
        cls,
        unit: str,
        aliases: list[str],
        pt_multiplier: float,
        const_enum: int,
    ) -> Self:
        if unit in cls.__instances__:
            instance: Self = cls.__instances__[unit]
            assert instance.pt_multiplier == pt_multiplier
            assert instance.const_enum == const_enum
            return instance
        return super().__new__(cls)

    def __str__(self):
        return f"<Unit {self.unit} [{self.const_enum}] = points * {self.pt_multiplier}>"

    def __init__(
        self,
        unit: str,
        aliases: list[str],
        pt_multiplier: float,
        const_enum: int,
    ) -> None:
        self.unit = unit
        self.aliases = aliases
        self.pt_multiplier = pt_multiplier
        self.const_enum = const_enum


class Unit(ChoiceEnumMixin, UnitType, Enum, metaclass=ChoiceEnumMeta):
    CENTIMETERS = ("CENTIMETERS", ["CM"], scribus.cm, scribus.UNIT_CM)
    CICERO = ("CICERO", ["CIC", "C"], scribus.c, scribus.UNIT_CICERO)
    INCHES = ("INCHES", ["IN", "INCH"], scribus.inch, scribus.UNIT_INCHES)
    MILLIMETERS = ("MILLIMETERS", ["MM"], scribus.mm, scribus.UNIT_MM)
    PICAS = ("PICAS", ["P", "PICA"], 1.0 / 12.0, scribus.UNIT_PICAS)
    POINTS = ("POINTS", ["PT", "POINT"], scribus.pt, scribus.UNIT_PT)

    def __hash__(self):
        return hash(self.__class__) + hash(self.name)

    def __new__(
        cls,
        name: str,
        aliases: list[str],
        pt_multiplier: float,
        const_enum: int,
    ) -> Self:
        instance = object.__new__(cls)
        object.__setattr__(
            instance,
            "_value_",
            UnitType(name, aliases, pt_multiplier, const_enum),
        )
        object.__setattr__(instance, "_name_", name)
        return instance

    @property
    def in_to_pt(self) -> float:
        return self.INCHES @ self.POINTS

    @override
    def __str__(self) -> str:
        return f"<UNIT {self.name} [{self.const_enum}] ({self.pt_multiplier})>"

    @classmethod
    def get_current(cls) -> Self:
        current_unit: int = scribus.getUnit()
        for unit in cls:
            if unit.const_enum == current_unit:
                return unit
        raise EnvironmentError(f"Could not determine Unit from {current_unit}")

    @classmethod
    def get(cls, key: str | int) -> Self:
        for u in cls:
            if u.value == key or u.name == key:
                return u
        raise KeyError(f"{key} not found")

    @classmethod
    def get_val(cls, key: str | int) -> UnitType:
        return cls.get_item(key)[1]

    @classmethod
    def get_item(cls, key: str | int) -> tuple[str, UnitType]:
        unit: Unit = cls.get(key)
        return (unit.name, unit.value)

    def __int__(self) -> int:
        return self.const_enum

    @override
    def __eq__(self, value: object, /) -> bool:
        return (
            value is self
            or value == self.const_enum
            or value == self.unit
            or value in self.aliases
        )

    def __matmul__(self, other: "Unit | UnitType") -> float:
        return other.pt_multiplier / self.pt_multiplier

    def __rmatmul__(self, other: "Unit | UnitType") -> float:
        return self.__matmul__(other, log=False)

    def __mul__(self, other: Number) -> float:
        return self.pt_multiplier * other

    def __rmul__(self, other: Number) -> float:
        return self.__mul__(other, False)
