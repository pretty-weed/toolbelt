import cProfile
import calendar
from collections import namedtuple
from dataclasses import dataclass, field, InitVar
from datetime import date, datetime, time, timedelta
from enum import Enum, StrEnum
from functools import cache, partial
from itertools import chain
from logging import basicConfig, getLogger, DEBUG, INFO, WARNING
from os import getenv
from pathlib import Path
from re import compile, Match
from typing import Collection, ClassVar, Iterator, Union

import scribus
import time
import yaml

# set up logging before local imports

LOG_PATH = Path().home().joinpath(".local", "tmp", "scribus-toolbelt-logs")
basicConfig(
    filename=str(LOG_PATH),
    encoding="utf-8",
    level=INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
)

from dandy_lib.datatypes.twodee import Size

import dandiscribe.colors as colors
from dandiscribe.enums import COLORS, FILL, PAGESIDE, FontFaces
from dandiscribe.data import Margins
from .data import Event, Task
from dandiscribe.layout import Page, SpreadPage
from dandiscribe.objects import Box, Column, ColumnSection
import dandiscribe.style as style
from dandiscribe.util import (
    cache_val,
    clear_cache_val,
    get_cache_val,
    ok_to_ignore_dialog,
    Debug,
    MISSING,
    PauseDrawing,
    TempGoTo,
)

import dandiscribe.calendar.data as data
from dandiscribe.calendar.pages import (
    gen_notes_spread_pages,
    A5FrontPage,
    A5MonthSpreadPage,
    A5NotesPage,
    A5WeekSpreadPage,
    MonthSpreadPage,
    WeekSpreadPage,
)

PROFILE = True

TIME_DELTA_RE = compile(r"^(\d+)([ymwd])$")
ROUTINES_FILE = Path(__file__).with_name("routines.yml")


ALL_DAYS = object()

logger = getLogger(__name__)
logger.setLevel(DEBUG)


@dataclass
class Document:
    pages: list[Page] = field(default_factory=list)
    masterpages: dict[str, Page] = field(default_factory=dict)

    def make(self):
        assert len(set(page.size for page in self.pages)) == 1
        if not scribus.newDocument(
            tuple(self.pages[0].size),
            (10, 10, 10, 15),
            scribus.PORTRAIT,
            1,
            scribus.UNIT_POINTS,
            scribus.PAGE_2,
            1,
            len(self.pages),
        ):
            raise NewDocError()

    def draw(
        self, tasks: list[Task] | None = None, events: list[Event] | None = None
    ):
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
            page.draw(
                master=False, tasks=tasks, events=events.get(page.page_date)
            )
            done += 1


def _delta_fom_match(orig: date, match: Match) -> timedelta:
    n, unit = match.groups()
    n = int(n)
    unit = unit.lower()

    try:
        if unit == "y":
            return date(orig.year + n, orig.month, orig.day) - orig
        elif unit == "m":
            zero_month = orig.month + n - 1
            res = (
                date(
                    orig.year + (zero_month // 12),
                    (zero_month % 12) + 1,
                    orig.day,
                )
                - orig
            )
            return res
        elif unit == "d":
            return timedelta(days=n)
        else:
            raise ValueError("unexpected unit")
    except ValueError as exc:
        raise ValueError(f"{orig} - {unit} - {n}") from exc


def load_routine_tasks(routines_file=ROUTINES_FILE) -> list[Task]:
    tasks = []
    routines_file = Path(routines_file)
    with routines_file.open("r") as fh:
        tasks = [
            Task.load({"title": task_name} | task)
            for task_name, task in yaml.safe_load(fh).items()
        ]
    return tasks


def prompt_to_date(prompt_str, start_date: datetime) -> datetime | date:

    match = TIME_DELTA_RE.match(prompt_str)

    if match:
        return start_date + _delta_fom_match(page_date, match)
    return date.fromisoformat(prompt_str.replace("/", "-").replace(".", "-"))


def make_doc(routines_file=ROUTINES_FILE) -> Document:
    # just do the thing for now
    logger.info("In make doc")
    tasks = load_routine_tasks(routines_file=routines_file)
    first_page_date = date.today()
    end = date(first_page_date.year, 12, 31)

    cached_prompt = get_cache_val("dates_prompt")
    dates_prompt = (
        cached_prompt if cached_prompt is not MISSING else end.isoformat()
    )

    logger.debug("Init dates prompt: %s", dates_prompt)
    dates_prompt = scribus.valueDialog(
        "date span/last date",
        f'{first_page_date.strftime("%Y/%m/%d")}-{end.strftime("%Y/%m/%d")}',
        dates_prompt,
    )

    logger.debug("res from first prompt: %s", dates_prompt)

    while dates_prompt:
        logger.debug("in while dates prompt %s %s", dates_prompt, end)
        if dates_prompt.count("-") % 2:
            # multiple dates:
            start_prompt, end_prompt = "/".join(
                dates_prompt.split("-")[: len(dates_prompt.split("-")) // 2]
            ), "/".join(
                dates_prompt.split("-")[len(dates_prompt.split("-")) // 2 :]
            )
        try:
            first_page_date = prompt_to_date(start_prompt, first_page_date)
            end = prompt_to_date(end_prompt, first_page_date)

        except ValueError:
            logger.exception("ValueError in loop", level=WARNING)
            dates_prompt = scribus.valueDialog(
                "End date", "yyyy[/.-]mm[/.-]dd".end.isoformat()
            )
        else:
            break

    else:
        # end prompt is empty, clear cache
        clear_cache_val("dates_prompt")
    if dates_prompt and dates_prompt != cached_prompt:
        cache_val("dates_prompt", dates_prompt, overwrite=True)
    logger.info("doing dates %s - %s", first_page_date, end)
    event_by_date = {}
    for event in Event.get_from_calendars(
        datetime.combine(first_page_date, time.min),
        datetime.combine(end, time.max),
    ):

        logger.info("handling event: %s", event)

        try:
            end_date, start_date = event.end.date(), event.start.date()
        except AttributeError:
            start_date, end_date = event.start, event.end
            start_time, end_time = time.min, time.max
        else:
            start_time, end_time = event.start.time(), event.end.time()

        if event.start == event.end:
            event_by_date.setdefault(start_date, []).append(event)
            continue

        try:
            extra_page = 1 if start_time >= end_time else 0
        except AttributeError:
            extra_page = 0
        for day_n in range((end_date - start_date).days + extra_page):
            event_by_date.setdefault(
                start_date + timedelta(days=day_n), []
            ).append(event)
        else:
            continue
    logger.info("starting pages")

    pages = [
        A5FrontPage(page_number=1, page_date=first_page_date),
        A5MonthSpreadPage(
            page_number=2,
            master_page=f"month-left",
            side=PAGESIDE.LEFT,
            page_date=first_page_date.replace(day=1),
        ),
        A5MonthSpreadPage(
            page_number=3,
            master_page=f"month-right",
            side=PAGESIDE.RIGHT,
            page_date=first_page_date.replace(day=1),
        ),
    ] + gen_notes_spread_pages(4)

    page_date = first_page_date
    # start on a monday
    while page_date.weekday():
        page_date -= timedelta(days=1)

    while page_date <= end:
        logger.info("doing page for %s", page_date)
        if (
            page_date.month != pages[-1].page_date.month
            and page_date.month > first_page_date.month
        ):
            pages += (
                gen_notes_spread_pages(len(pages) + 1, factory=A5NotesPage)
                + [
                    A5MonthSpreadPage(
                        page_number=len(pages) + page_add + 3,
                        master_page=f"month-{side}",
                        side=side,
                        page_date=page_date.replace(day=1),
                    )
                    for page_add, side in enumerate(
                        [PAGESIDE.LEFT, PAGESIDE.RIGHT]
                    )
                ]
                + gen_notes_spread_pages(len(pages) + 5, factory=A5NotesPage)
            )

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
        page_date += timedelta(days=7)
    pages += gen_notes_spread_pages(len(pages) + 1)

    doc = Document(pages)

    doc.make()
    colors.register_colors()
    with PauseDrawing():
        doc.draw(tasks, event_by_date)
        # Checkbox.clean()


class NewDocError(Exception):
    pass


def entry_point(routines_file=ROUTINES_FILE, profile=PROFILE, debug=False):
    logger.info("entered entry point")
    with Debug("main", enabled=debug) as main_debug:
        if profile:
            profile_path = (
                Path()
                .home()
                .joinpath(".local", "tmp", "scribus_calendar.profile")
            )
            with cProfile.Profile() as profile:
                make_doc(routines_file=routines_file)
                profile.dump_stats(profile_path)
        else:
            make_doc(routines_file=routines_file)


if __name__ == "__main__":
    entry_point()
