from dataclasses import dataclass, field, InitVar, MISSING

import datetime
from logging import getLogger, INFO
from pathlib import Path
from typing import Optional, Collection

from dandiscribe.enums import COLORS
from dandiscribe.objects import Box, ColumnSection
import dandiscribe.style as style

from .data import Event, Task, TIME_OF_DAY

logger = getLogger(__name__)
logger.setLevel(INFO)


@dataclass(kw_only=True)
class WeekCalToDSection(ColumnSection):

    time_of_day: TIME_OF_DAY = MISSING

    @classmethod
    def factory(
        cls,
        rows: int,
        sub_rows: int,
        time_of_day: TIME_OF_DAY,
        tasks: Collection[Task] = field(default_factory=[]),
        events: Collection[Event] = field(default_factory=[]),
        check_boxes: bool = True,
        background: Optional[COLORS] = None,
        remaining_spaces: int = 2,
        title_style: (
            style.TextStyle | style.ParagraphStyle
        ) = style.WEEK_CAL_TOD_HDR_STYLE,
        title_line_style: style.LineStyle | None = None,
        task_style: (
            style.TextStyle | style.ParagraphStyle
        ) = style.WEEK_CAL_TASK_STYLE,
    ):
        tasks = [task for task in tasks or [] if task in time_of_day]
        logger.debug(f"post filter tasks ({time_of_day}): {tasks}")
        if len(tasks) > (rows * sub_rows - remaining_spaces):
            raise ValueError(f"Too many tasks {len(tasks)} for calendar day!")
        pre_fill = []
        while tasks:
            pre_fill.append([])
            while tasks and len(pre_fill[-1]) < sub_rows:
                task = tasks.pop()
                pre_fill_text = task.title
                try:
                    pre_fill_text = f'{task.routine_time.time_of_day.strftime("%H:%M")}: {pre_fill_text}'
                except AttributeError as exc:
                    # this is okay, we're assuming this is a TIME OF DAY
                    pass
                pre_fill[-1].append(pre_fill_text)

        boxes = [
            Box(
                rows=rows,
                sub_rows=sub_rows,
                check_boxes=check_boxes,
                pre_fill=pre_fill,
                pre_fill_style=task_style,
                pre_fill_max_lines=1,
                draw_cb_func=lambda r, sr: ((r * sub_rows) + sr) % 3,
            )
        ]
        return cls(
            time_of_day=time_of_day,
            boxes=boxes,
            background=background,
            title=time_of_day.name.split()[0].title(),
            title_style=title_style,
            title_line_style=title_line_style,
        )


@dataclass(kw_only=True)
class MonthDay(ColumnSection):
    date: datetime.date
    tasks: InitVar[list[Task]] = None
    events: InitVar[list[Event]] = None
    past_month_color: InitVar[str] = COLORS.GREY

    @classmethod
    def create(
        cls,
        day: int,
        week: int,
        first_date: datetime.date,
        page_month: int,
        tasks: list[Task] | None = None,
        past_month_color: str = COLORS.GREY,
        **kwargs,
    ):
        if tasks is None:
            tasks = []
        day_date = first_date + datetime.timedelta(days=day, weeks=week)
        if day_date.month != page_month:
            kwargs["background"] = past_month_color
        kwargs["title"] = day_date.strftime(
            f"%d{' (%b)' if day_date.month != page_month else ''}"
        ).strip("0")

        return cls(
            tasks=tasks,
            date=day_date,
            past_month_color=past_month_color,
            title_style=style.MONTH_DATE_PSTYLE,
            title_in_master=False,
            **kwargs,
        )
