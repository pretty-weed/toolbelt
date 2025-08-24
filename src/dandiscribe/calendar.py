import cProfile
import calendar
from collections import namedtuple
from copy import copy
from dataclasses import dataclass, field, InitVar
import datetime
from enum import Enum, StrEnum
from functools import partial
from itertools import chain
from os import getenv
from pathlib import Path
from re import compile, Match
from typing import Collection, ClassVar, Iterator, Union

import scribus
import time
import yaml

from dandiscribe.enums import COLORS, FILL, PAGESIDE
from dandiscribe.data import frozen_dataclass, LineStyle, Margins, Size
from dandiscribe.layout import Page, SpreadPage
from dandiscribe.objects import Box, ColumnSection
from dandiscribe.util import Debug, PauseDrawing, TempGoTo

PROFILE = True

TIME_DELTA_RE = compile(r"^(\d+)([ymwd])$")
ROUTINES_FILE = Path(__file__).with_name("routines.yml")


_Duration = namedtuple("Duration", ["start", "end"])


class Duration(_Duration):
    def __contains__(
        self, other: Union[datetime.time, datetime.datetime, "Duration"]
    ) -> bool:
        try:
            # If this is a datetime
            other = other.time()
        except AttributeError:

            try:
                return self.start <= other.start and other.end < self.end
            except AttributeError:
                pass
        # not durations

        # This replace ensures that `other` is a time,
        # when we check this way
        return start < other.replace(second=0) < end

    def __and__(self, other):
        early, late = sorted([self, other], key=lambda x: x.start)
        if early.end < late.start:
            raise ValueError(f"NO NO NO {early}, {late} ({self}, {other})")
            return None

        return Duration(max(early.start, late.start), min(early.end, late.end))

    def __or__(self, other):
        early, late = sorted([self, other], key=lambda x: x.start)
        if early.end < late.start:
            # disjoint
            raise ValueError(f"NO NO NO {early}, {late} ({self}, {other})")
            return None

        return Duration(
            min(early.start, late.start), max(early.start, late.start)
        )

    @classmethod
    def create(
        cls,
        start_hour: int,
        end_hour: int,
        start_minute: int = 0,
        end_minute: int = 0,
    ):
        return cls(
            datetime.time(start_hour, start_minute),
            datetime.time(end_hour, end_minute),
        )
class TIME_OF_DAY(Enum):
    OVERNIGHT_MORNING = Duration.create(start_hour=0, end_hour=5)
    EARLY_MORNING = Duration.create(start_hour=5, end_hour=8)
    MORNING = Duration.create(start_hour=5, end_hour=12)
    ALL_MORNING = MORNING | OVERNIGHT_MORNING
    LATE_MORNING = Duration.create(
        start_hour=10, start_minute=30, end_hour=11, end_minute=30
    )
    NOON = Duration.create(
        start_hour=11, start_minute=30, end_hour=12, end_minute=30
    )
    EARLY_AFTERNOON = Duration.create(start_hour=12, end_hour=2, end_minute=30)
    AFTERNOON = Duration.create(start_hour=12, end_hour=5)
    LATE_AFTERNOON = Duration.create(start_hour=16, end_hour=17)
    EARLY_EVENING = Duration.create(start_hour=5, end_hour=18)
    EVENING = Duration.create(start_hour=5, end_hour=20)
    LATE_EVENING = Duration.create(start_hour=19, end_hour=20)
    NIGHT = Duration.create(start_hour=20, end_hour=0)
    EVENING_AND_NIGHT = EVENING | NIGHT

    def __contains__(
        self, other: datetime.datetime | datetime.time | Duration
    ) -> bool:

        # If this is a task, get duration from task
        try:
            other = other.routine_time.time_of_day
        except AttributeError:
            pass
        else:
            return other in self.duration
        try:
            return self.start <= other.start and self.end <= other.end
        except AttributeError:
            # either datetime or time
            try:
                # if it's datetime, make it a time
                other = other.time()
            except AttributeError:
                pass
            try:
                if self.start <= other <= self.end:
                    return True
            except TypeError as exc:
                raise TypeError(f"Not comparable") from exc

        return False

    def match(
        self,
        time: datetime.datetime | datetime.time,
        duration: datetime.timedelta | int = None,
    ) -> bool:
        try:
            # this will work for datetime.datetime
            time = time.time()
        except AttributeError:
            # excepted for datetime.datetime, treat time as a `time()`
            pass

        if duration is None:
            time_end = time
        else:
            try:
                time_end = time + duration
            except TypeError:
                # an int
                time_end = time + datetime.timedelta(hours=duration)

        # Start is after end, is overnight
        if self.start > self.end:
            return time <= start or time_end > end
        return start <= time and time_end < end



@frozen_dataclass
class RoutineTime:
    weekdays: list[int]
    time_of_day: TIME_OF_DAY
    weeks: list[int] | None = None

    @classmethod
    def load(cls, in_dict):
        in_dict = dict(
            (k.lower(), v) for k, v in in_dict.items() if k in cls.__dataclass_fields__
        )
        if "time_of_day" in in_dict:
            in_dict["time_of_day"] = TIME_OF_DAY[in_dict["time_of_day"]]

        return cls(**({"weekdays": [], "weeks": [], "time_of_day": None,} | in_dict))

    def match(
        self,
        day: datetime.date | datetime.datetime | int,
        time: datetime.time | datetime.datetime | int,
        week: int = None,
        duration: datetime.timedelta | int = None,
    ) -> bool:

        if (
            week is not None
            and self.weeks is not None
            and week not in self.weeks
        ):
            return False

        # if date is a datetime
        try:
            date = date.date()
        except AttributeError:
            # either int (day of week) or day
            pass

        try:
            day = date.weekday
        except AttributeError:
            # assume is int
            if not 0 <= day <= 6:
                raise ValueError("Day must be 0-6 for day of week")

        # if time is a datetime
        if time is not None:
            try:
                time = time.time()
            except AttributeError:
                # might be a time, might be an int
                # try int
                try:
                    time = datetime.time(hour=time)
                except TypeError:
                    # time is a time, presumably
                    pass

            if duration is not None:
                try:
                    duration = datetime.timedelta(hours=duration)
                except TypeError:
                    # duration is already a delta
                    pass

            if not self.time_of_day.match(time, duration):
                return False


@frozen_dataclass
class Task:
    title: str
    description: str = None
    due: datetime.date = None
    routine_time: RoutineTime = None

    def __post_init__(self):
        if self.due is None and self.routine_time is None:
            raise TypeError("either due or routine time must not be None")
        elif self.due is not None and self.routine_time is not None:
            raise TypeError(
                "routine time and due may not both be set on a Task"
            )

    @classmethod
    def load(cls, in_dict):
        in_dict = dict(
            (k.lower(), v) for k, v in in_dict.items() if k in cls.__dataclass_fields__
        )
        if "due" in in_dict:
            in_dict["due"] = datetime.date.fromisoformat(in_dict["due"])
        if "routine_time" in in_dict:
            in_dict["routine_time"] = RoutineTime.load(in_dict)
        return cls(**in_dict)


def tasks_by_routine_day(tasks: list[Task]) -> dict[int, set[Task]]:
    sorted_tasks = {}
    for task in tasks:
        if task.routine_time is None:
            continue
        for weekday in task.routine_time.weekdays:
            sorted_tasks.setdefault(routine_day, set()).add(task)
    return sorted_tasks


def get_tasks(
    tasks: list[Task],
    date: datetime.date,
    time_of_day: TIME_OF_DAY = None,
    remove_routine: bool = False,
) -> Iterator[Task]:
    if remove_routine:
        tasks = [task for task in tasks if not task.routine_time]
    for task in tasks:
        if task.day == date.weekday() and (
            (time_of_day is None) or (task in time_of_day)
        ):
            yield task


def get_month_tasks(
    tasks: list[Task], date: datetime.date, remove_routine: bool = True
) -> Iterator[Task]:
    # TODO get previous month tasks on calendar (back to prev monday)
    dow, last_day = calendar.monthrange(date.year, date.month)
    for day in range(1, last_day + 1):
        yield from get_tasks(
            tasks, date.replace(day=day), remove_routine=remove_routine
        )
        dow = (dow + 1) % 7


@frozen_dataclass
class WeekCalToDsection(ColumnSection):

    time_of_day: TIME_OF_DAY

    @classmethod
    def factory(
        cls,
        time_of_day: TIME_OF_DAY,
        tasks: Collection[Task],
        rows: int,
        sub_rows: int,
        check_boxes: bool = True,
        background: COLORS = True,
        remaining_spaces: int = 2,
    ):

        tasks = [task for task in tasks or [] if task in self.time_of_day]
        if len(tasks) > (rows * sub_rows - remaining_spaces):
            raise ValueError(f"Too many tasks {len(tasks)} for calendar day!")
        pre_fill = []
        while tasks:
            pre_fill.append([])
            while tasks and len(pre_fill[-1]) < len(sub_rows):
                pre_fill[-1].append(tasks.pop().title)

        boxes = [
            Box(
                rows=rows,
                sub_rows=sub_rows,
                check_boxes=check_boxes,
                pre_fill=pre_fill,
            )
        ]
        return cls(time_of_day=time_of_day, boxes=boxes, background=background)


@frozen_dataclass
class MonthDay(ColumnSection):
    day: InitVar[int]
    week: InitVar[int]
    page_date: InitVar[datetime.date]

    tasks: InitVar[list[Task]] = None
    past_month_color: InitVar[str] = COLORS.GREY

    @classmethod
    def create(
        cls,
        day: int,
        week: int,
        page_date: datetime.date,
        tasks: list[Task] = None,
        past_month_color: str = COLORS.GREY,
        **kwargs,
    ):
        if tasks is None:
            tasks = []
        day_date = page_date + datetime.timedelta(days=day, weeks=week)
        if day_date.month != page_date.month:
            kwargs["background"] = past_month_color
        kwargs["title"] = day_date.strftime("%d -- %B(%y)").strip("0")

        return cls(
            day=day,
            week=week,
            page_date=page_date,
            past_month_color=past_month_color,
            **kwargs,
        )


@frozen_dataclass
class Column:
    sections: list[ColumnSection] = field(default_factory=list)
    divider_line: LineStyle = None

    @property
    def rows(self):
        return sum(section.rows for section in self.sections)

    def draw(self, x: int, y: int, width: int, height: int, master=None):
        rows = self.rows
        row_height = height // rows

        for section in self.sections:
            section.draw(x, y, width, row_height * section.rows, master=master)
            y += row_height * section.rows
            if master or master is None:

                if (
                    section != self.sections[-1]
                    and self.divider_line is not None
                ):
                    section_divider = scribus.createLine(x, y, x + width, y)
                    scribus.setLineWidth(
                        self.divider_line.weight, section_divider
                    )
                    scribus.setLineStyle(
                        self.divider_line.style, section_divider
                    )



@frozen_dataclass
class CalendarPage(Page):
    page_date: datetime.date = field(default_factory=datetime.date.today)

    def __post_init__(self):
        if self.page_date.weekday():
            raise ValueError(
                f"{self.page_date} is not a Monday ({self.page_date.weekday()})"
            )

    def draw(self, master=None, tasks: Collection[Task] = None):
        return super().draw(master)


@frozen_dataclass
class WeekSpreadPage(CalendarPage, SpreadPage):
    padding: int = 5
    _GUTTER = Column(
                    sections=[
                        ColumnSection(height_rows=1),
                        ColumnSection(
                            title="Priorities",
                            boxes=[Box(rows=2, sub_rows=2)],
                            title_in_master=True,
                        ),
                        ColumnSection(
                            title="To Do",
                            boxes=[Box(rows=6, sub_rows=2, check_boxes=True)],
                            title_in_master=True,
                        ),
                        ColumnSection(
                            title="Notes", height_rows=6, title_in_master=True
                        ),
                    ]
                )
    def draw(self, master=None, tasks: list[Task] = None):
        super().draw(master=master)
        draw_master = master is None or bool(master)

        margins, usable_size = self._get_margins_and_usable_size()
        usable_width, usable_height = usable_size
        tasks_by_week_day = tasks_by_routine_day(tasks)
        with self:
            # only one horizontal padding col
            col_width = (usable_width - self.padding) // 4

            x = margins.left

            if self.side is PAGESIDE.LEFT:
                # left side gutter
                self._GUTTER.draw(
                    margins.left,
                    margins.top,
                    col_width,
                    usable_height,
                    master=master,
                )

                week_of_date = copy(self.page_date)
                while week_of_date.weekday():
                    week_of_date -= datetime.timedelta(days=1)
                eow_date = week_of_date + datetime.timedelta(6)
                if not draw_master:
                    weekof_text = scribus.createText(margins.left + 3, margins.top + 3, col_width, 20)
                    scribus.setText(f"Week of {week_of_date.strftime('%B %d')} to {eow_date.strftime('%B %d, %Y')}", weekof_text)
                    scribus.setFontSize(8, weekof_text)
                    
                # TODO probably get these from builtin modules
                days = ["Monday", "Tuesday", "Wednesday"]
                x += col_width + self.padding
            else:
                days = ["Thursday", "Friday", "Saturday", "Sunday"]
            col_date = self.page_date
            for day in days:
                # Draw the column itself
                col = Column(
                    sections=[
                        WeekCalToDsection.factory(
                            time_of_day=time_of_day,
                            tasks=tasks_by_week_day.get(col_date.weekday()),
                            rows=3,
                            sub_rows=2,
                            check_boxes=True,
                            background=section_bg,
                        )
                        for section_bg, time_of_day in [
                            (COLORS.LIGHT_BLUE, TIME_OF_DAY.ALL_MORNING),
                            (COLORS.WHITE, TIME_OF_DAY.AFTERNOON),
                            (COLORS.PINK, TIME_OF_DAY.EVENING_AND_NIGHT),
                        ]
                    ]
                )

                col.draw(
                    x, margins.top, col_width, usable_height, master=master
                )
                x += col_width
                col_date += datetime.timedelta(days=1)


@frozen_dataclass
class MonthSpreadPage(CalendarPage, SpreadPage):
    header_height: int = 36
    day_name_height: int = 12
    padding: int = 5

    def draw(self, master=None, tasks: list[Task] = None):

        # Only display tasks that don't happen every week
        # bit of an editorial descision whatevs
        tasks = [task for task in tasks if (not task.routine_time or not task.routine_time.weeks)]

        super().draw(master=master)
        margins, usable_size = self._get_margins_and_usable_size()
        usable_width, usable_height = usable_size
        draw_master = master is None or bool(master)
        with self:

            col_width = usable_width // 4

            row_height = usable_height // 5

            if self.side == PAGESIDE.RIGHT:
                col_week_days = [5, 6, 7]

            else:
                col_week_days = [1, 2, 3, 4]

            cal_cols = dict(
                (
                    day,
                    Column(
                        sections=[
                            MonthDay.create(
                                day=day,
                                week=week,
                                page_date=self.page_date,
                                boxes=[Box(rows=3, sub_rows=2)],
                                # todo "due" tasks
                                tasks=[t for t in tasks if t.routine_time is not None and day in t.routine_time.weekdays and week in t.routine_time.weeks],
                            )
                            for week in range(5)
                        ],
                        divider_line=LineStyle(weight=1.5, style=1),
                    ),
                )
                for day in col_week_days
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
                scribus.setText(
                    (self.page_date + datetime.timedelta(days=7)).strftime(
                        f"%B - {self.page_date}"
                    ),
                    month_name,
                )

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


A5WeekSpreadPage = partial(WeekSpreadPage, size=Size(*scribus.PAPER_A5))
A5MonthSpreadPage = partial(MonthSpreadPage, size=Size(*scribus.PAPER_A5))

A5FrontPage = partial(CalendarPage, size=Size(*scribus.PAPER_A5))


@dataclass
class Document:
    pages: list[Page] = field(default_factory=list)
    masterpages: dict[str, Page] = field(default_factory=dict)

    def make(self):
        assert len(set(page.size for page in self.pages)) == 1
        if not scribus.newDocument(
            tuple(self.pages[0].size),
            (10, 10, 10, 20),
            scribus.PORTRAIT,
            1,
            scribus.UNIT_POINTS,
            scribus.PAGE_2,
            1,
            len(self.pages),
        ):
            raise NewDocError()

    def draw(self, tasks: list[Task] | None = None):
        # make master pages
        scribus.progressReset()
        mp_count = len(set(page.master_page for page in self.pages))
        total = mp_count + len(self.pages)
        done = 0
        for page in self.pages:
            if page.master_page not in self.masterpages:

                scribus.progressSet((done + 1) // total)
                master_page = page.as_master_page()
                self.masterpages[page.master_page] = master_page
                master_page.draw(master=True, tasks=tasks)
                done += 1

                assert all([pg.is_master for pg in self.masterpages.values()])
                assert not any([pg.is_master for pg in self.pages])

        # make pages
        for page in self.pages:
            scribus.progressSet((done + 1) // total)
            page.draw(master=False, tasks=tasks)
            done += 1


def _delta_fom_match(orig: datetime.date, match: Match) -> datetime.timedelta:
    n, unit = match.groups()
    n = int(n)
    unit = unit.lower()

    try:
        if unit == "y":
            return datetime.date(orig.year + n, orig.month, orig.day) - orig
        elif unit == "m":
            zero_month = orig.month + n - 1
            res = (
                datetime.date(
                    orig.year + (zero_month // 12),
                    (zero_month % 12) + 1,
                    orig.day,
                )
                - orig
            )
            return res
        elif unit == "d":
            return datetime.timedelta(days=n)
        else:
            raise ValueError("unexpected unit")
    except ValueError as exc:
        raise ValueError(f"{orig} - {unit} - {n}") from exc


def make_doc(routines_file=ROUTINES_FILE) -> Document:
    # just do the thing for now
    tasks = []
    routines_file = Path(routines_file)
    with routines_file.open("r") as fh:
        tasks = [
            Task.load({"title": task_name} | task)
            for task_name, task in yaml.safe_load(fh).items()
        ]
    

    page_date = datetime.date.today()
    # start on a monday
    while page_date.weekday():
        page_date += datetime.timedelta(days=1)
    end = datetime.date(page_date.year, 12, 31)
    end_prompt = scribus.valueDialog(
        "End date", "yyyy[/.-]mm[/.-]dd", end.isoformat()
    )

    while end_prompt:
        match = TIME_DELTA_RE.match(end_prompt)
        if match:
            end = page_date + _delta_fom_match(page_date, match)
            break
        try:
            end = datetime.date.fromisoformat(
                end_prompt.replace("/", "-").replace(".", "-")
            )
        except ValueError:
            end_prompt = scribus.valueDialog(
                "End date", "yyyy[/.-]mm[/.-]dd".end.isoformat()
            )
        else:
            break

    pages = [
        A5FrontPage(page_number=1, page_date=page_date),
        A5MonthSpreadPage(
            page_number=2,
            master_page=f"month-left",
            side=PAGESIDE.LEFT,
            page_date=page_date,
        ),
        A5MonthSpreadPage(
            page_number=3,
            master_page=f"month-right",
            side=PAGESIDE.RIGHT,
            page_date=page_date,
        ),
    ]
    while page_date <= end:
        if page_date.month != pages[-1].page_date.month:
            pages += [
                A5MonthSpreadPage(
                    page_number=len(pages) + page_add + 1,
                    master_page=f"month-{side}",
                    side=side,
                    page_date=page_date,
                )
                for page_add, side in enumerate([PAGESIDE.LEFT, PAGESIDE.RIGHT])
            ]

        pages += [
            A5WeekSpreadPage(
                page_number=len(pages) + 1,
                master_page="week-left",
                side=PAGESIDE.LEFT,
                page_date=page_date,
            ),
            A5WeekSpreadPage(
                page_number=len(pages) + 2,
                master_page="week-right",
                side=PAGESIDE.RIGHT,
                padding=5,
                page_date=page_date,
            ),
        ]
        page_date += datetime.timedelta(days=7)

    doc = Document(pages)

    doc.make()

    with PauseDrawing():
        doc.draw(tasks)
        # Checkbox.clean()


class NewDocError(Exception):
    pass


def main(routines_file=ROUTINES_FILE, profile=PROFILE, debug=False):
    with Debug("main", enabled=debug) as main_debug:
        if profile:
            profile_path = (
                Path().home().joinpath(".local", "tmp", "scribus_calendar.profile")
            )
            with cProfile.Profile() as profile:
                make_doc(routines_file=routines_file)
                profile.dump_stats(profile_path)
        else:
            make_doc(routines_file=routines_file)


if __name__ == "__main__":
    main()
