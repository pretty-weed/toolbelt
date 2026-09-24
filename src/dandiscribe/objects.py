from collections.abc import Callable
from dataclasses import dataclass, field
from logging import getLogger
from typing import ClassVar, cast

import scribus
from dandy_lib.datatypes.twodee import Size

from dandiscribe.data import Align
from dandiscribe.enums import FILL, HAlignSimple, VAlign, VAlignSimple
from dandiscribe.exceptions import DrawError, TooShort
from dandiscribe.style import LineStyle, ParagraphStyle, TextStyle
from dandiscribe.util import (
    TempGoTo,
    get_justify_adjustments,
)

logger = getLogger(__name__)


class _Drawable:
    def draw(self, x: int, y: int, width: int, height: int, master: bool):
        assert all(n >= 0 for n in [x, y, width, height])
        _ = master

    def _keep_drawing(
        self, x: int, y: int, width: int, height: int, master: bool
    ) -> bool:
        _ = x = y = width = height
        _ = master
        return False


class Drawable(_Drawable):
    def _keep_drawing(
        self, x: int, y: int, width: int, height: int, master: bool, **kwargs
    ) -> bool:
        try:
            super().draw(x=x, y=y, width=width, height=height, master=master)
        except TypeError as exc:
            raise TypeError("Unexpected vars") from exc
        except AttributeError as exc:
            logger.exception("Error drawing [%s]: %s", self, exc)
            raise AttributeError(f"Error drawing {self}") from exc
        else:
            return True


@dataclass
class HasBadge(Drawable):

    badge_path: str | None = None
    badge_halign: HAlignSimple = HAlignSimple.RIGHT
    badge_valign: VAlignSimple = VAlignSimple.TOP
    badge_pad: float = 0.0625 / scribus.inch
    badge_in_master: bool = False
    badge_size: float = 0.125 / scribus.inch

    def draw(
        self, x: int, y: int, width: int, height: int, master: bool, **kwargs
    ):
        self.draw_badge(x, y, width, height, master)
        self._keep_drawing(x, y, width, height, master, **kwargs)

    def draw_badge(self, x: int, y: int, width: int, height: int, master: bool):
        if self.badge_path and master == self.badge_in_master:
            badge_x = width - self.badge_pad - self.badge_size

            badge_frame = scribus.createImage(
                badge_x, y + self.badge_pad, self.badge_size, self.badge_size
            )

            scribus.loadImage(self.badge_path, badge_frame)
            scribus.setScaleImageToFrame(True, True, badge_frame)
            scribus.setFillColor("None", badge_frame)
            scribus.setLineColor("None", badge_frame)


@dataclass
class HasTitle(Drawable):
    title: str | None = None
    title_style: TextStyle | ParagraphStyle | None = None
    title_min_y: int = 0
    title_height: int | None = None
    title_line_style: LineStyle | None = None
    title_in_master: bool = True

    def __post_init__(self, *args, **kwargs):
        logger.debug("HasTitle PostInit: args: %s; kwargs; %s", args, kwargs)
        if self.title is not None:
            if self.title_height is None:
                raise ValueError("title height must not be none if has a title")
            if self.title_height < self.title_min_y:
                raise TooShort(self.title_min_y, self.title_height)

    def draw_title(
        self, x: int, y: int, width: int, height: int, master: bool
    ) -> tuple[str, list[str]] | None:
        if master == self.title_in_master and self.title is not None:
            objects = []
            if self.title_height is not None:
                if self.title_height > height:
                    raise TooShort(self.title_height, height, self)
            elif height < self.title_min_y:
                logger.exception(
                    f"{height} too short for {self.title} (need {self.title_min_y})"
                )
                raise TooShort(self.title_min_y, height, self)
            print(
                "Creating title box[%s]: x: %d, y: %d, %d x %d"
                % (self.title, x, y, width, height)
            )
            title_box = scribus.createText(x, y, width, self.title_height)

            scribus.setText(self.title, title_box)
            if self.title_style is not None:
                self.title_style.apply(title_box)
            scribus.setTextVerticalAlignment(scribus.ALIGNV_BOTTOM, title_box)

            if self.title_line_style is not None:
                title_line = scribus.createLine(
                    x, y + height, x + width, y + height
                )
                self.title_line_style.apply(title_line)
                objects.append(title_line)

            return title_box, objects


@dataclass
class Box(Drawable):
    rows: int = 1
    sub_rows: int = 1
    row_style: LineStyle = LineStyle(weight=0.75, style=1)
    sub_row_style: LineStyle = LineStyle(weight=0.5, style=6)
    check_boxes: bool = False
    pre_fill: list[list[str]] = field(default_factory=list)
    align: Align = field(default_factory=Align)
    name: str | None = None
    pre_fill_style: TextStyle | ParagraphStyle = None
    pre_fill_max_lines: int | None = None
    join_lines_with_next: bool = False
    line_extra_length: int = 0
    draw_cb_func: Callable = None

    def __post_init__(self):
        if self.sub_rows < 1:
            raise ValueError("sub rows must be greater than or equal to one")

    def draw(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        master=None,
        prefill_from_bottom: bool = False,
        pre_fill_max_lines: int | None = None,
    ):

        if pre_fill_max_lines is None:
            pre_fill_max_lines = self.pre_fill_max_lines
        draw_master = master is None or bool(master)
        objects: list[str] = []
        row_height = height // (self.rows)
        sub_row_height = row_height // self.sub_rows
        cb = Checkbox(
            size=Size.factory(sub_row_height // 3),
            style=LineStyle(style=1, weight=0.5),
        )

        if self.align.vertical is VAlign.JUSTIFIED:
            height_adj = get_justify_adjustments(
                self.rows, self.height % self.rows
            )
        else:
            height_adj = [0] * self.rows

        for row, row_height_adj in zip(range(self.rows), height_adj):

            this_row_height = row_height + row_height_adj
            row_y = y + (row * this_row_height)
            if prefill_from_bottom and self.rows - 1 - row < len(self.pre_fill):
                row_prefill = self.pre_fill[self.rows - 1 - row]
            elif not prefill_from_bottom and row < len(self.pre_fill):
                row_prefill = self.pre_fill[row]
            else:
                row_prefill = None

            if draw_master and self.check_boxes:
                if self.draw_cb_func is None or self.draw_cb_func(row, 0):
                    row_cb = scribus.setItemName(
                        f"RowCB: {row}",
                        cb.draw(
                            x + sub_row_height // 4,
                            row_y + sub_row_height // 3 + sub_row_height,
                        ),
                    )
                    objects.append(row_cb)

            for sub_row in range(self.sub_rows):
                sr_x = x
                sub_row_y = row_y + (sub_row * sub_row_height)

                # mebbe not needed
                if draw_master:
                    if not sub_row == self.sub_rows - 1:
                        # draw dashed line between sub rows

                        sub_line = scribus.createLine(
                            x,
                            sub_row_y + sub_row_height,
                            x + width + self.line_extra_length,
                            sub_row_y + sub_row_height,
                        )
                        objects.append(sub_line)
                        if self.sub_row_style.style is not None:
                            scribus.setLineStyle(
                                self.sub_row_style.style, sub_line
                            )
                        scribus.setLineWidth(
                            self.sub_row_style.weight, sub_line
                        )

                if self.check_boxes:
                    if (
                        draw_master
                        and self.draw_cb_func is not None
                        and self.draw_cb_func(row, sub_row + 1)
                    ):
                        objects.append(
                            scribus.setItemName(
                                f"subrow_cb {row}.{sub_row}",
                                cb.draw(
                                    sr_x + sub_row_height // 4,
                                    sub_row_y + sub_row_height // 3,
                                ),
                            )
                        )
                    sr_x += sub_row_height // 2 + sub_row_height // 3

                if not draw_master and row_prefill is not None:
                    if prefill_from_bottom:
                        prefill_idx = self.sub_rows - sub_row - 1

                    else:
                        prefill_idx = sub_row
                    if prefill_idx < len(row_prefill):
                        # pre-fill if necessary
                        # last -10 is pretty arbirary
                        objects.append(
                            scribus.createText(
                                sr_x,
                                sub_row_y,
                                width - cb.size.width - 3,
                                sub_row_height,
                            )
                        )
                        scribus.setText(row_prefill[sub_row], objects[-1])
                        if self.pre_fill_style is not None:
                            self.pre_fill_style.apply(objects[-1])
                        scribus.layoutText(objects[-1])
                        font_size = scribus.getFontSize(objects[-1])
                        while pre_fill_max_lines is not None and (
                            scribus.getTextLines(objects[-1])
                            > pre_fill_max_lines
                            or scribus.getFrameText(objects[-1])
                            != scribus.getAllText(objects[-1])
                        ):
                            logger.info(
                                "objects 139: pf_ml: %s (%s) %s, %s",
                                scribus.getFrameText(objects[-1]),
                                font_size,
                                pre_fill_max_lines,
                                scribus.getTextLines(objects[-1]),
                            )
                            font_size -= 0.5
                            scribus.setFontSize(font_size, objects[-1])

                            scribus.layoutText(objects[-1])
                        logger.info(
                            "objects 143: pf_ml: %s - %s(%s, %s) %s, %s",
                            scribus.getFrameText(objects[-1]),
                            scribus.getAllText(objects[-1]),
                            scribus.getFontSize(objects[-1]),
                            font_size,
                            pre_fill_max_lines,
                            scribus.getTextLines(objects[-1]),
                        )

            # Row line (bottom)
            if draw_master:
                line = scribus.createLine(
                    x,
                    row_y + this_row_height,
                    x + width + self.line_extra_length,
                    row_y + this_row_height,
                )
                objects.append(line)
                scribus.setLineStyle(self.row_style.style, line)
                scribus.setLineWidth(self.row_style.weight, line)

        if not objects:
            return None
        if len(objects) == 1:
            return objects[0]
        group = scribus.groupObjects(list(set(objects)))
        if self.name is not None:
            group = scribus.setItemName(self.name, group)
        return group


@dataclass
class Checkbox:
    size: Size
    style: LineStyle

    _cache: ClassVar[dict[(Size, LineStyle), (str, int)]] = dict()
    SCRATCH_PAGE: ClassVar[int] = 1
    GOTO1: ClassVar[TempGoTo] = TempGoTo(1)

    @classmethod
    def _get(
        cls, size: Size, style: LineStyle, x: int, y: int
    ) -> tuple[str, bool]:
        try:
            return cls._cache[(size, style)], False
        except KeyError:
            with cls.GOTO1:
                cls._cache[(size, style)] = draw_checkbox(
                    x, y, size=size, style=style
                )
            return cls._cache[(size, style)], True

    def draw(self, x: int, y: int) -> str:
        cb_ref, _new = self._get(self.size, self.style, x, y)
        try:
            with self.GOTO1 as current:
                scribus.copyObjects([cb_ref])
        except scribus.NoValidObjectError as exc:
            raise ValueError(
                "failed to copy checkbox. ref: {cb_ref}, page:{scribus.currentPage()}, objects: {scribus.getAllObjects()}",
            ) from exc

        new_cb = scribus.pasteObjects()
        assert len(new_cb) == 1
        scribus.moveObjectAbs(x, y, new_cb[0])

        return new_cb[0]

    @classmethod
    def clean(cls):
        current = scribus.currentPage()
        scribus.gotoPage(cls.SCRATCH_PAGE)
        for scribus_obj in cls._cache:
            raise ValueError("cleaning")
            scribus.DeleteObject(scribus_obj)
        cls._cache.clear()
        scribus.gotoPage(current)


def draw_checkbox(x: int, y: int, size: Size, style: LineStyle) -> str:
    # toDo : style
    corner_len = (size.width // 4, size.height // 4)
    bot = y + size.height
    right = x + size.width
    lines = []
    polygon_name = scribus.createPolyLine(
        [x, y + corner_len[1], x, y, x + corner_len[0], y]
    )
    lines.append(polygon_name)
    lines.append(
        scribus.createPolyLine(
            [right - corner_len[0], y, right, y, right, y + corner_len[1]]
        )
    )
    lines.append(
        scribus.createPolyLine(
            [right, bot - corner_len[1], right, bot, right - corner_len[0], bot]
        )
    )
    lines.append(
        scribus.createPolyLine(
            [x, bot - corner_len[1], x, bot, x + corner_len[0], bot]
        )
    )
    scribus.deselectAll()
    for line in lines:
        scribus.selectObject(line)
    scribus.setLineWidth(style.weight)
    scribus.combinePolygons()
    return scribus.setItemName(f"CB({size.width}x{size.height}", polygon_name)


@dataclass
class ColumnSection(HasBadge, HasTitle):
    fill: FILL = FILL.CLEAR
    background: str | None = None
    boxes: list[Box] = field(default_factory=list)
    # extra "rows" for calculating section height
    height_rows: int = 0
    box_align: Align = field(default_factory=Align)

    @property
    def rows(self):
        # int bool title is 1 if there is a title, 0 if not
        return (
            int(bool(self.title))
            + self.height_rows
            + sum(box.rows * box.sub_rows for box in self.boxes)
        )

    def draw(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        master: bool | None = None,
    ) -> str:

        objects = []
        if master is not None:
            master = bool(master)
        if master is not False and self.background is not None:
            bg_box = scribus.createRect(x, y, width, height, "colBG")
            scribus.setFillColor(self.background, bg_box)
            objects.append(bg_box)
        # TODO fill

        rows = self.rows + int(bool(self.title))
        row_height = height // rows
        box_y = y

        if self.title:
            try:
                self.draw_title(x, y, width, height=row_height, master=master)
            except TooShort as exc:
                self.draw_title(
                    x, y, width, height=int(exc.minimum), master=master
                )
                rows = self.rows
                row_height = (height - exc.minimum) // rows
                box_y += exc.minimum
            else:
                box_y += row_height

        if self.box_align.vertical is VAlign.JUSTIFIED:
            # fill out the adjustments
            justify_adjustments = get_justify_adjustments(
                len(self.boxes), height % len(self.boxes)
            )
        else:
            justify_adjustments = [0] * len(self.boxes)

        self.draw_badge(x, y, width, height, master)

        for box, height_adjustment in zip(self.boxes, justify_adjustments):
            box_height = (
                row_height * box.rows * box.sub_rows + height_adjustment
            )
            box_object = box.draw(
                x, box_y, width - 10, box_height, master=master
            )
            if box_object is not None:
                objects.append(box_object)

            box_y += box_height

        if len(objects) > 1:
            try:
                group = scribus.groupObjects(objects)
            except scribus.NoValidObjectError as exc:
                raise ValueError(str(objects)) from exc
            if self.title:
                return scribus.setItemName(self.title, group)
        elif objects and self.title:
            return scribus.setItemName(self.title, objects[0])


@dataclass
class Column(HasBadge, HasTitle):
    sections: list[ColumnSection] = field(default_factory=list)
    divider_line: LineStyle | None = None

    @property
    def rows(self):
        return sum(section.rows for section in self.sections)

    def draw(
        self, x: int, y: int, width: int, height: int, master=None, **kwargs
    ):
        row_y = y
        if self.title is not None and height < self.title_height:
            raise DrawError(
                f"{height} is less than title min draw size:{self.title_min_y}"
            )
        super().draw(
            x=x, y=y, width=width, height=height, master=master, **kwargs
        )
        rows = self.rows
        if self.title:
            row_y += cast(int, self.title_height)
            # since self.title is defined, self.title_height must not be None
            row_height = (height - cast(int, self.title_height)) // rows
            self.draw_title(x, y, width, height, master)
            print(f"drew title {self.title} at {x}x{y}, set row_y to {row_y}")
        else:
            print(f"Not drwing title for column {self}")
            row_height = height // rows

        for section in self.sections:
            section.draw(
                x, row_y, width, row_height * section.rows, master=master
            )
            row_y += row_height * section.rows
            if master or master is None:

                if (
                    section != self.sections[-1]
                    and self.divider_line is not None
                ):
                    section_divider = scribus.createLine(x, y, x + width, y)
                    self.divider_line.apply(section_divider)
