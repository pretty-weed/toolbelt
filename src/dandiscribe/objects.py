from dataclasses import field
from typing import ClassVar

import scribus

from dandiscribe.data import frozen_dataclass, LineStyle, Size
from dandiscribe.enums import FILL
from dandiscribe.util import ok_to_ignore_dialog, TempGoTo

@frozen_dataclass
class Box:
    rows: int = 1
    sub_rows: int = 1
    row_style: LineStyle = LineStyle(weight=0.75, style=1)
    sub_row_style: LineStyle = LineStyle(weight=0.5, style=6)
    check_boxes: bool = False
    pre_fill: list[list[str]] = field(default_factory=list)

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
    ):
        draw_master = master is None or bool(master)
        objects = []
        row_height = height // self.rows
        sub_row_height = row_height // self.sub_rows
        cb = Checkbox(
            size=Size.factory(sub_row_height // 3),
            style=LineStyle(style=1, weight=0.5),
        )

        for row in range(self.rows):

            if prefill_from_bottom and self.rows - 1 - row in self.pre_fill:
                row_prefill = self.pre_fill[self.rows - 1 - row]
            elif not prefill_from_bottom and row in self.pre_fill:
                row_prefill = self.pre_fill[row]
            else:
                row_prefill = None

            row_y = y + (row * row_height)

            for sub_row in range(self.sub_rows - 1):
                print(f'sub row objects: {objects}')
                sr_x = x

                sub_row_y = row_y + (sub_row * sub_row_height)
                # mebbe not needed
                if not sub_row == self.sub_rows - 1:
                    # draw dashed line between sub rows

                    if draw_master:
                        sub_line = scribus.createLine(
                            x,
                            sub_row_y + sub_row_height,
                            x + width,
                            sub_row_y + sub_row_height,
                        )
                        objects.append(sub_line)
                        scribus.setLineStyle(self.sub_row_style.style, sub_line)
                        scribus.setLineWidth(
                            self.sub_row_style.weight, sub_line
                        )

                if self.check_boxes and draw_master:
                    objects.append(
                        cb.draw(
                            sr_x + sub_row_height // 4,
                            sub_row_y + sub_row_height // 3,
                        )
                    )
                    sr_x += sub_row_height // 2 + sub_row_height //3
                    

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
                                sub_row_y + sub_row_height // 3,
                                width - cb.size.width - 10,
                            )
                        )
                        objects.append(scribus.setText(row_prefill[sub_row_i], objects[-1]))

            # Row line
            if draw_master:
                line = scribus.createLine(
                    x, row_y + row_height, x + width, row_y + row_height
                )
                objects.append(line)
                scribus.setLineStyle(self.row_style.style, line)
                scribus.setLineWidth(self.row_style.weight, line)
                if self.check_boxes:
                    objects.append(
                        cb.draw(
                            x + sub_row_height // 4,
                            row_y + sub_row_height // 3 + sub_row_height,
                        )
                    )
        
        if not objects:
            return None

        try:
            return scribus.groupObjects(objects)
        except Exception as exc:
            raise ValueError(str(objects))


@frozen_dataclass
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
                "foo",
                f"ref: {cb_ref}, page:{scribus.currentPage()}, objects: {scribus.getAllObjects()}",
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

    return polygon_name


@frozen_dataclass
class ColumnSection:
    title: str = ""
    fill: FILL = FILL.CLEAR
    background: str | None = None
    boxes: list[Box] = field(default_factory=list)
    # extra "rows" for calculating section height
    height_rows: int = 0
    title_in_master: bool = True

    @property
    def rows(self):
        # int bool title is 1 if there is a title, 0 if not
        return (
            int(bool(self.title is not None))
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
            bg_box = scribus.createRect(x, y, width, height)
            scribus.setFillColor(self.background, bg_box)
            objects.append(bg_box)
        # TODO fill
        rows = self.rows
        row_height = height // rows
        if self.title:
            if master == self.title_in_master:
                title_box = scribus.createText(x, y, width - 10, row_height - 2)
                objects.append(title_box)
                scribus.setText(self.title, title_box)
                scribus.setFontSize(row_height // 2, title_box)
                scribus.setTextVerticalAlignment(
                    scribus.ALIGNV_BOTTOM, title_box
                )
            if master or master is None:
                # pre-fill if necessary
                title_line = scribus.createLine(
                    x, y + row_height, x + width - 10, y + row_height
                )
                objects.append(title_line)
                scribus.setLineWidth(2, title_line)

            y += row_height

        for box in self.boxes:
            box_height = row_height * box.rows * box.sub_rows
            box_object = box.draw(x, y, width - 10, box_height, master=master)
            if box_object is not None:
                objects.append(box_object)

            y += box_height

        if len(objects) > 1:
            try:
                group = scribus.groupObjects(objects)
            except scribus.NoValidObjectError as exc:
                raise ValueError(str(objects)) from exc
            scribus.setItemName(self.title, group)
        elif objects:
            scribus.setItemName(self.title, objects[0])

        objects = []
