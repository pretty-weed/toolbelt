from .data import Event as Event, Task as Task
from _typeshed import Incomplete
from collections import namedtuple as namedtuple
from dandiscribe.calendar.pages import A5FrontPage as A5FrontPage, A5MonthSpreadPage as A5MonthSpreadPage, A5NotesPage as A5NotesPage, A5WeekSpreadPage as A5WeekSpreadPage, MonthSpreadPage as MonthSpreadPage, WeekSpreadPage as WeekSpreadPage, gen_notes_spread_pages as gen_notes_spread_pages
from dandiscribe.data import Margins as Margins
from dandiscribe.enums import COLORS as COLORS, FILL as FILL, FontFaces as FontFaces, PAGESIDE as PAGESIDE
from dandiscribe.exceptions import NewDocError as NewDocError
from dandiscribe.layout import Page as Page, SpreadPage as SpreadPage
from dandiscribe.objects import Box as Box, Column as Column, ColumnSection as ColumnSection
from dandiscribe.util import Debug as Debug, MISSING as MISSING, PauseDrawing as PauseDrawing, TempGoTo as TempGoTo, cache_val as cache_val, clear_cache_val as clear_cache_val, get_cache_val as get_cache_val, ok_to_ignore_dialog as ok_to_ignore_dialog
from dataclasses import InitVar as InitVar, dataclass, field
from datetime import date, datetime
from enum import Enum as Enum, StrEnum as StrEnum
from functools import cache as cache, partial as partial
from itertools import chain as chain
from os import getenv as getenv

LOG_PATH: Incomplete
PROFILE: bool
TIME_DELTA_RE: Incomplete
ROUTINES_FILE: Incomplete
ALL_DAYS: Incomplete
logger: Incomplete

@dataclass
class Document:
    pages: list[Page] = field(default_factory=list)
    masterpages: dict[str, Page] = field(default_factory=dict)
    def make(self) -> None: ...
    def draw(self, tasks: list[Task] | None = None, events: list[Event] | None = None): ...

def load_routine_tasks(routines_file=...) -> list[Task]: ...
def prompt_to_date(prompt_str, start_date: datetime) -> datetime | date: ...
def make_doc(routines_file=...) -> Document: ...
def entry_point(routines_file=..., profile=..., debug: bool = False) -> None: ...
