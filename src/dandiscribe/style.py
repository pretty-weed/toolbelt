from dataclasses import dataclass, field
from typing import ClassVar
import scribus

from dandy_lib.datatypes.numeric import bounded_int_factory, NonNegInt

import dandiscribe.colors
import dandiscribe.enums as enums
from dandiscribe.util import ok_to_ignore_dialog

ZeroToOnehundredInt = bounded_int_factory(0, 100)
FullIntensity = ZeroToOnehundredInt(100)


@dataclass(frozen=True)
class LineStyle:
    weight: NonNegInt
    style: int | None = None

    def apply(self, obj):
        scribus.setLineWidth(self.weight, obj)
        if self.style is not None:
            scribus.setLineStyle(self.style, obj)


OnePointBlackLine = LineStyle(weight=1, style=1)
TwoPointBlackLine = LineStyle(weight=2, style=1)


@dataclass
class FillStyle:
    color: dandiscribe.colors.COLORS
    shade: ZeroToOnehundredInt = FullIntensity

    def __post_init__(self, shade: ZeroToOnehundredInt = FullIntensity):
        # check this
        ZeroToOnehundredInt(self.shade)


NO_FILL = FillStyle(color=enums.COLORS.NONE)

@dataclass
class ObjectStyle:
    fill: FillStyle

@dataclass(frozen=True)
class TextStyle:
    _inited: ClassVar[dict[str, bool]] = {}
    name: str
    font: str | None = None
    size: float | None = None
    features: list[enums.FontFeature] = field(default_factory=list)
    fill_color: enums.COLORS = enums.COLORS.RICH_BLACK
    stroke_color: enums.COLORS = enums.COLORS.NONE

    def new_with(self, new_name: str, font: str | None = None, size: float | None = None, features: list[enums.FontFeature] = None, fill_color: str = None, stroke_color: str = None):
        return self.__class__(new_name, font if font is not None else self.font, size if size is not None else self.size, features if features is not None else self.features, fill_color if fill_color is not None else self.fill_color, stroke_color if stroke_color is not None else self.stroke_color)

    def setup(self):
        if not self.name in scribus.getCharStyles():
            style_kwargs = {}
            if self.font is not None:
                try:
                    style_kwargs["font"] = self.font.value
                except AttributeError as exc:
                    scribus.valueDialog("foo", str(exc))
                    style_kwargs["font"] = self.font
            if self.size is not None:
                style_kwargs["fontsize"] = self.size
            if self.features:
                style_kwargs["features"] = ",".join(self.features)
            try:
                scribus.createCharStyle(
                    name=self.name,
                    fillcolor=self.fill_color,
                    strokecolor = self.stroke_color,
                    **style_kwargs,
                )
            except ValueError as exc:
                raise ValueError(f"Failed to create Text style {self.name}: {self}") from exc

        self._inited[self.name] = True
    def apply(self, apply_obj):
        if not self._inited.get(self.name):
            self.setup()
        scribus.setCharacterStyle(self.name, apply_obj)



WEEK_CAL_DAY_HDR_STYLE = TextStyle(
    "Week Cal Day Header",
    font=enums.FontFaces.CHANCERY_BOLD,
    size=13,
    features=[enums.FontFeature.UNDERLINEWORDS]
)

WEEK_OF_MAIN_STYLE = TextStyle(
    "Main Week of",
    font=enums.FontFaces.CHANCERY_MED,
    size=10,
)

MONTH_DATE_TSTYLE = TextStyle(
    "Month Date",
    font=enums.FontFaces.CHANCERY_MED,
    size=6,
)


@dataclass
class ParagraphStyle:
    _inited: ClassVar[dict[str, bool]] = {}
    name: str
    linespacing_mode: enums.LinespacingMode = enums.LinespacingMode.AUTOMATIC
    alignment: enums.HAlign = enums.HAlign.LEFT
    vert_alignment: enums.VAlign = None
    left_margin: int = 0
    right_margin: int = 0
    gap_before: int = 0
    gap_after: int = 0
    first_indent: int = 0
    has_drop_cap: bool = False
    drop_cap_lines: int = None
    drop_cap_offset: int = None
    char_style: TextStyle = None


    def new_with(
        self, new_name: str,
        linespacing_mode: enums.LinespacingMode=None,
        alignment: enums.HAlign = None,
        vert_alignment: enums.VAlign = None,
        left_margin: int = None,
        right_margin: int = None,
        gap_before: int = None,
        gap_after: int = None,
        first_indent: int = None,
        has_drop_cap: int = None,
        drop_cap_lines: int = None,
        drop_cap_offset: int = None,
        char_style: TextStyle = None):
        return self.__class__(
            new_name, 
            linespacing_mode if linespacing_mode is not None else self.linespacing_mode,
            alignment if alignment is not None else self.alignment,
            vert_alignment if vert_alignment is not None else self.vert_alignment,
            left_margin if left_margin is not None else self.left_margin,
            right_margin if right_margin is not None else self.right_margin,
            gap_before if gap_before is not None else self.gap_before,
            gap_after if gap_after is not None else self.gap_after,
            first_indent if first_indent is not None else self.first_indent,
            has_drop_cap if has_drop_cap is not None else self.has_drop_cap,
            drop_cap_lines if drop_cap_lines is not None else self.drop_cap_lines,
            drop_cap_offset if drop_cap_offset is not None else self.drop_cap_offset,
            char_style if char_style is not None else self.char_style,
        )

    def setup(self):
        if not self.name in scribus.getParagraphStyles():
            style_kwargs = {}
            if self.linespacing_mode is not None:
                style_kwargs["linespacingmode"] = self.linespacing_mode
            if self.alignment is not None:
                style_kwargs["alignment"] = self.alignment
            if self.left_margin is not None:
                style_kwargs["leftmargin"] = self.left_margin
            if self.right_margin is not None:
                style_kwargs["rightmargin"] = self.right_margin
            if self.gap_before is not None:
                style_kwargs["gapbefore"] = self.gap_before
            if self.gap_after is not None:
                style_kwargs["gapafter"] = self.gap_after
            if self.first_indent is not None:
                style_kwargs["firstindent"] = self.first_indent
            if self.has_drop_cap is not None:
                style_kwargs["hasdropcap"] = int(self.has_drop_cap)
            if self.drop_cap_lines is not None:
                style_kwargs["dropcaplines"] = self.drop_cap_lines
            if self.drop_cap_offset is not None:
                style_kwargs["dropcapoffset"] = self.drop_cap_offset
            if self.char_style is not None:
                style_kwargs["charstyle"] = self.char_style.name

            scribus.createParagraphStyle(
                name=self.name,
                **style_kwargs,
            )

        self._inited[self.name] = True
    def apply(self, apply_obj):
        if self.char_style is not None:
            self.char_style.setup()
        if not self._inited.get(self.name):
            self.setup()
        if self.vert_alignment is not None:
            scribus.setTextVerticalAlignment(self.vert_alignment, apply_obj)
        scribus.setParagraphStyle(self.name, apply_obj)


WEEK_CAL_TOD_HDR_STYLE = ParagraphStyle(
    "Week Cal ToD Header",
    left_margin=5, char_style=WEEK_CAL_DAY_HDR_STYLE.new_with(
    "Week Cal ToD Header",
    font=enums.FontFaces.CHANCERY_ITALIC,
    size=10,
    features=[]
))

WEEK_CAL_READINGS_STYLE = WEEK_CAL_TOD_HDR_STYLE.new_with("Week Cal Readings", char_style=WEEK_CAL_TOD_HDR_STYLE.char_style.new_with("Week Cal Readings", font=enums.FontFaces.CHANCERY_MED))

MONTH_CAL_HEADER_STYLE = ParagraphStyle(
    "Month Cal Header",
    char_style=TextStyle(
        "Month Cal Header",
        font=enums.FontFaces.CHANCERY_BOLD,
        size=19,
        features=[enums.FontFeature.UNDERLINEWORDS]
    )
)
MONTH_CAL_HEADER_STYLE_RALIGN = MONTH_CAL_HEADER_STYLE.new_with("Month Cal Header Right", alignment=enums.HAlign.RIGHT)
MONTH_CAL_DAY_HDR_STYLE = MONTH_CAL_HEADER_STYLE.new_with("Month Cal day hdr", char_style=MONTH_CAL_HEADER_STYLE.char_style.new_with("Month Cal Day Hdr", size=13))

WEEK_CAL_TASK_STYLE = ParagraphStyle(
    "Week Cal Task",
    vert_alignment=enums.VAlign.CENTERED,
    char_style=TextStyle(
        "Week Cal Task", 
        font=enums.FontFaces.CHANCERY_MED, 
        size=8.0)
)

MONTH_DATE_PSTYLE = ParagraphStyle(
    "Month Date",
    left_margin=5, char_style=MONTH_DATE_TSTYLE
)

GUTTER_HEADER_STYLE = TextStyle(
    "Gutter Column Header",
    font=enums.FontFaces.CHANCERY_MED,
    size=12,
)


def fill_lined_basic(x, y, width, height, draw_master: bool, line_height: int = 13, line_style: LineStyle=OnePointBlackLine):
    if draw_master is not None and not draw_master:
        return None
        
    lines = []
    for line_y in range(int(y), int(y+height+1), line_height):
        line=scribus.createLine(x, line_y, x+width, line_y)
        line_style.apply(line)
        lines.append(line)

    return scribus.groupObjects(lines)



FILLERS = frozenset([fill_lined_basic])