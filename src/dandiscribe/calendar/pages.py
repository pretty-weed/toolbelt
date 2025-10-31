from copy import copy
from dataclasses import dataclass, field
import datetime
from functools import partial
import random
from typing import Collection, Callable

from dandy_lib.datatypes.twodee import Size

from dandiscribe.objects import Box, Column, ColumnSection
from dandiscribe.data import Margins 
from dandiscribe.calendar.data import get_events, get_tasks, tasks_by_routine_day_and_time, Event, Task, TIME_OF_DAY
from dandiscribe.calendar.layout import MonthDay, WeekCalToDsection
from dandiscribe.enums import COLORS, FontFaces, PAGESIDE, HAlign
from dandiscribe.layout import SpreadPage, Page
import dandiscribe.style as style

from .data import Task, Event

import scribus

@dataclass(kw_only=True)
class CalendarPage(Page):
    page_date: datetime.date = field(default_factory=datetime.date.today)
    def draw(self, master=None, tasks: Collection[Task] = None, events: Collection[Event] = None):
        return super().draw(master)

@dataclass(kw_only=True)
class SpreadPage(Page):
    inside_margin: int = 30
    outside_margin: int = 10
    side: PAGESIDE

    def _get_margins_and_usable_size(self):
        margins, usable_size = super()._get_margins_and_usable_size()
        usable_size.width = self.size.width - self.inside_margin - self.outside_margin
        if self.side is PAGESIDE.LEFT:
            margins = margins.with_right(self.inside_margin).with_left(self.outside_margin)
        else:
            margins = margins.with_left(self.inside_margin).with_right(self.outside_margin)
        return margins, usable_size
        

@dataclass(kw_only=True)
class NotesSpread(CalendarPage, SpreadPage):
    columns: int = 1
    rows: int = 1
    row_max_offset: int = 0
    col_max_offset: int = 0
    fillers: dict[float, Callable] = field(default_factory=lambda: {0.5: copy(style.FILLERS)})


    def draw(self, master=None, tasks: list[Task] = None, events: dict[datetime.datetime, Event] = None):
        
        super().draw(master=master)
        with self:
            margins, usable_size = self._get_margins_and_usable_size()
            usable_width, usable_height = usable_size
            draw_master = master is None or bool(master)

            # just do the damn thing for now
            if draw_master:
                title = scribus.createText(margins.left, margins.top, usable_width, 19)
                scribus.setText("Notes…", title)
                if self.side == PAGESIDE.LEFT:
                    style.MONTH_CAL_HEADER_STYLE.apply(title)
                else:
                    style.MONTH_CAL_HEADER_STYLE_RALIGN.apply(title)
                return style.fill_lined_basic(margins.left, margins.top+ 20, usable_width, usable_height - 21, draw_master)



@dataclass(kw_only=True)
class MonthSpreadPage(CalendarPage, SpreadPage):
    header_height: int = 36
    day_name_height: int = 12

    def __post_init__(self):
        if self.side is None or self.side is MISSING:
            raise TypeError("side must be provided as keyword")

    padding: int = 5
    def __post_init__(self):
        if self.page_date.day != 1:
            raise ValueError(
                f"{self.page_date} is not the first of the month ({self.page_date.weekday()})"
            )

    def draw(self, master=None, tasks: list[Task] = None, events: dict[datetime.datetime, Event] = None):

        # Only display tasks that don't happen every week
        # bit of an editorial descision whatevs
        tasks = [task for task in tasks if (not task.routine_time or not task.routine_time.weeks)]
        if events is None:
            events = {}
        super().draw(master=master)
        margins, usable_size = self._get_margins_and_usable_size()
        usable_width, usable_height = usable_size
        draw_master = master is None or bool(master)
        first_date = self.page_date - datetime.timedelta(days=self.page_date.weekday()  + 1)
        page_month = self.page_date.month
        with self:

            col_width = usable_width // 4

            row_height = usable_height // 5

            if self.side == PAGESIDE.RIGHT:
                col_week_days = zip(range(5, 8), ["Friday", "Saturday", "Sunday"])

            else:
                col_week_days = list((day_i + 1, day_name) for day_i, day_name in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday"]))
            
            cal_cols = dict(
                (
                    day,
                    Column(
                        
                        sections=[
                            ColumnSection(title=day_name, title_in_master=True, 
                            title_style=style.MONTH_CAL_DAY_HDR_STYLE, 
                            title_line_style=style.LineStyle(2), title_min_y=16)] + [
                        ] +[
                            MonthDay.create(
                                day=day,
                                week=week,
                                first_date=first_date,
                                boxes=[Box(rows=3, sub_rows=2)],
                                page_month=page_month,
                                # todo "due" tasks
                                tasks=get_tasks(tasks, first_date + datetime.timedelta(days=day, weeks=week), remove_routine=True),
                                events=events.get(first_date + datetime.timedelta(days=day, weeks=week), [])
                            )
                            for week in range(5)
                        ],
                        divider_line=style.LineStyle(weight=1.5, style=1),
                    ),
                )
                for day, day_name in col_week_days
            )
            if not draw_master:
                month_name = scribus.createText(
                    margins.left + 20, margins.top + 20, usable_width - 40, 35
                )
                if self.side is PAGESIDE.LEFT:
                    align = scribus.ALIGN_LEFT
                else:
                    align = scribus.ALIGN_RIGHT
                scribus.setTextAlignment(align, month_name)
                if self.page_date.day == 1:
                    month_start_date = self.page_date
                else:
                    month_start_date = self.page_date.replace(day=1, month=self.page_date.month % 12 + 1)
                scribus.setText(
                    month_start_date.strftime("%B"),
                    month_name,
                )
                if self.side == PAGESIDE.LEFT:
                    style.MONTH_CAL_HEADER_STYLE.apply(month_name)
                else:
                    style.MONTH_CAL_HEADER_STYLE_RALIGN.apply(month_name)


            x = margins.left
            for col in cal_cols.values():
                col.draw(
                    x,
                    margins.top + 55,
                    col_width,
                    usable_height - 55,
                    master=master,
                )
                x += col_width


# TODO: Move this where it belongs

def _getdate(in_dt_or_date: datetime.datetime | datetime.date) -> datetime.date:
    try:
        return in_dt_or_date.date
    except AttributeError:
        return in_dt_or_date

@dataclass(kw_only=True)
class WeekSpreadPage(CalendarPage, SpreadPage):
    def __post_init__(self):
        if self.page_date.weekday():
            raise ValueError(
                f"{self.page_date} is not a Monday ({self.page_date.weekday()})"
            )

    padding: int = 5
    _GUTTER = Column(
                    sections=[
                        ColumnSection(
                            title="Priorities",
                            boxes=[Box(rows=2, sub_rows=2)],
                            title_in_master=True,
                            title_style=style.GUTTER_HEADER_STYLE,
                        ),
                        ColumnSection(
                            title="To Do",
                            title_style=style.GUTTER_HEADER_STYLE,
                            boxes=[Box(rows=2, sub_rows=6, check_boxes=True, draw_cb_func = lambda r, sr: sr % 3)],
                            title_in_master=True,
                        ),
                        ColumnSection(
                            title="Notes", height_rows=6, title_in_master=True,
                            title_style=style.GUTTER_HEADER_STYLE,
                        ),
                    ]
                )
    def draw(self, master=None, tasks: list[Task] = None, events: list[Event] = None):
        super().draw(master=master)
        if events is None:
            events = []
        draw_master = master is None or bool(master)

        margins, usable_size = self._get_margins_and_usable_size()
        usable_width, usable_height = usable_size
        tasks_by_day_and_time = tasks_by_routine_day_and_time(tasks, valid_times=[TIME_OF_DAY.MORNING, TIME_OF_DAY.AFTERNOON, TIME_OF_DAY.EVENING_AND_NIGHT])

        
        gutter_height = usable_height - 40
        col_height = usable_height - 20
        with self:
            # only one horizontal padding col
            col_width = usable_width // 4 - self.padding

            x = margins.left

            if self.side is PAGESIDE.LEFT:
                # left side gutter
                self._GUTTER.draw(
                    margins.left,
                    margins.top + 40,
                    col_width,
                    gutter_height,
                    master=master,
                )

                # =============================================================
                # # Gutter header
                # 
                # Week of
                # _________ to _________ 
                # <year>
                # =============================================================
                
                week_of_date = copy(self.page_date)
                while week_of_date.weekday():
                    week_of_date -= datetime.timedelta(days=1)
                eow_date = week_of_date + datetime.timedelta(6)
                if not draw_master:
                    weekof_text = scribus.createText(margins.left, margins.top + 3, col_width + 3, 40)
                    start_mo, end_mo = (d.strftime("%b") + ("." if d.strftime("%B") != d.strftime("%b") else "") for d in (week_of_date, eow_date))
                    scribus.setText(f"   Week of\n{week_of_date.strftime(f'{start_mo} %d')}-{eow_date.strftime(f'{end_mo} %d\n   %Y')}", weekof_text)

                    scribus.selectText(0,0, weekof_text)
                    scribus.setLineSpacing(12, weekof_text)
                    scribus.setFontSize(10, weekof_text)
                    scribus.selectText(0,10, weekof_text)
                    scribus.setFont(FontFaces.CHANCERY_MED, weekof_text)
                    scribus.selectText(10, scribus.getTextLength(weekof_text)-14, weekof_text)
                    scribus.setFont("QTChanceryType Bold", weekof_text)
                    scribus.setFontSize(12, weekof_text)
                    scribus.selectText(scribus.getTextLength(weekof_text)-7, 7, weekof_text)
                    scribus.setFont("QTChanceryType Medium", weekof_text)
                    scribus.selectText(0,0, weekof_text)

                # TODO probably get these from builtin modules
                day_offsets = range(3)
                x += col_width + self.padding
            else:
                day_offsets = range(3, 7)

            # Start creating the columns
            for day_offset in day_offsets:
                col_date = self.page_date + datetime.timedelta(days=day_offset)
                col = Column(
                    sections=[
                        ColumnSection(
                            title=col_date.strftime(f"%A.{col_date.day}"), 
                            title_style=style.WEEK_CAL_DAY_HDR_STYLE,
                            title_in_master=False,
                            title_line_style=style.LineStyle(2))] + [
                        WeekCalToDsection.factory(
                            time_of_day=time_of_day,
                            tasks=tasks_by_day_and_time.get(col_date.weekday(), dict()).get(time_of_day, set()),
                            events=[evt for evt in events if _getdate(evt.start) <= col_date <= _getdate(evt.end)],
                            rows=3 if time_of_day == TIME_OF_DAY.AFTERNOON else 2,
                            sub_rows=3,
                            check_boxes=True,
                            background=section_bg,
                        )
                        for section_bg, time_of_day in [
                            (COLORS.PINK, TIME_OF_DAY.MORNING),
                            (COLORS.WHITE, TIME_OF_DAY.AFTERNOON),
                            (COLORS.LIGHT_BLUE, TIME_OF_DAY.EVENING_AND_NIGHT),
                        ]] + [
                            ColumnSection(
                                title="Readings" if day_offset < 5 else ("Notes…" if day_offset == 5 else "\t"),
                                title_style=style.WEEK_CAL_READINGS_STYLE,
                                boxes=[Box(
                                    rows=1 if day_offset < 5 else 2,
                                    sub_rows=4 if day_offset < 5 else 2,
                                    join_lines_with_next=day_offset==6,
                                    line_extra_length=self.padding * 2 if day_offset==5 else 0,
                                    check_boxes=day_offset<5,
                                    pre_fill_max_lines=1,
                                    draw_cb_func=lambda r, sr: sr != 2
                                )]
                        )]
                        
                )

                col.draw(
                    x, margins.top + 20, col_width, col_height -1, master=master
                )
                x += col_width
                col_date += datetime.timedelta(days=1)



A5WeekSpreadPage = partial(WeekSpreadPage, size=Size(*scribus.PAPER_A5))
A5MonthSpreadPage = partial(MonthSpreadPage, size=Size(*scribus.PAPER_A5))

A5FrontPage = partial(CalendarPage, size=Size(*scribus.PAPER_A5))
A5NotesPage = partial(NotesSpread, size=Size(*scribus.PAPER_A5))

def gen_notes_spread_pages(left_page_number, factory=NotesSpread) -> list[NotesSpread]:
    return [
        
        factory(
            page_number=left_page_number,
            master_page="notes-left",
            side=PAGESIDE.LEFT,
        ),
        factory(
            page_number=left_page_number + 1,
            master_page="notes-right",
            side=PAGESIDE.RIGHT,
        ),
    ]