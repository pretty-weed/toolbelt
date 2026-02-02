import dandiscribe.style as style
import datetime
from .data import Event as Event, TIME_OF_DAY as TIME_OF_DAY, Task as Task
from _typeshed import Incomplete
from dandiscribe.enums import COLORS as COLORS
from dandiscribe.objects import Box as Box, ColumnSection as ColumnSection
from dataclasses import InitVar, dataclass
from pathlib import Path as Path
from typing import Collection

logger: Incomplete

@dataclass(kw_only=True)
class WeekCalToDSection(ColumnSection):
    time_of_day: TIME_OF_DAY = ...
    @classmethod
    def factory(cls, rows: int, sub_rows: int, time_of_day: TIME_OF_DAY, tasks: Collection[Task] = ..., events: Collection[Event] = ..., check_boxes: bool = True, background: COLORS | None = None, remaining_spaces: int = 2, title_style: style.TextStyle | style.ParagraphStyle = ..., title_line_style: style.LineStyle | None = None, task_style: style.TextStyle | style.ParagraphStyle = ...): ...

@dataclass(kw_only=True)
class MonthDay(ColumnSection):
    date: datetime.date
    tasks: InitVar[list[Task]] = ...
    events: InitVar[list[Event]] = ...
    past_month_color: InitVar[str] = ...
    @classmethod
    def create(cls, day: int, week: int, first_date: datetime.date, page_month: int, tasks: list[Task] | None = None, past_month_color: str = ..., **kwargs): ...
