import datetime
from enum import auto, unique, Enum, IntEnum, StrEnum

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
