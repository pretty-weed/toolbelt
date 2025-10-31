# get events from calendar url 
from collections import namedtuple
from dataclasses import dataclass
import datetime
from enum import Enum
from functools import cache
from logging import getLogger, INFO
from os import getenv
from pathlib import Path, PurePath
from typing import Any, Iterator, Union
from urllib.parse import urlparse, ParseResult

from yaml import safe_load
from requests import get
from requests.exceptions import ConnectionError
from icalendar import Calendar, Event


CONF_FILE = Path(getenv("CONF_FILE", Path().home().joinpath(".private", "calendars.yaml")))
CalEvent = namedtuple("CalEvent", ["calendar", "event"])
logger = getLogger(__name__)
logger.setLevel(INFO)
def get_conf(filepath: Path = CONF_FILE) -> dict[str: any]:
    if not CONF_FILE.exists or not CONF_FILE.read_text():
        return {}

    return safe_load(CONF_FILE.read_text())

def get_calendars() -> dict[str, Calendar]:
    calendars = {}
    for calendar, url in get_conf().get("external_calendars", {}).items():
        try:
            res = get(url)
        except ConnectionError:
            logger.exception("Failed to get calendar")
        else:
            calendars[calendar] = Calendar.from_ical(res.text)
    return calendars


def _date_and_dt_key(in_val: datetime.date | datetime.datetime) -> datetime.datetime:
    try:
        return datetime.datetime.combine(in_val.date(), in_val.time())
    except AttributeError:
        # in_val is date
        return datetime.datetime.combine(in_val, datetime.time.min)

def get_events(
        start: datetime.date, 
        end: datetime.date,
        collated: bool = True, 
        calendar:str = None) -> Iterator[CalEvent]:

    if collated:
        events = []
    for calendar_name, calendar in get_calendars().items():
        if collated:
            events.extend(CalEvent(calendar, event) for event in calendar.events)
        else:
            for event in calendar.events:
                # force start to a datetime
                yield CalEvent(calendar, event)
    
    if collated:

        yield from sorted(events, key=lambda cv: _date_and_dt_key(cv.event.start))


_Duration = namedtuple("Duration", ["start", "end"])


class Duration(_Duration):
    def __contains__(
        self, other: Union[datetime.time, datetime.datetime, "Duration"]
    ) -> bool:

        try:
            other = other.value
        except AttributeError:
            pass
        try:
            # Deal with other as routinetime
            other_tod = other.time_of_day
        except AttributeError as exc:
            # deal with other as either duration, time of day, datetime, or time
            try:
                # deal with other as duration or time of day
                # these should be datetime or time
                other_start = other.start
                other_end = other.end
            except AttributeError:
                # Deal with other as datetime or time
                other_start = other_end = other
                

        else:
            other_start = other_tod.start
            other_end = other_tod.end
            

        try:
            # at this point, other start and other end should either be
            # datetime or time
            other_start = other_start.time().replace(second=0)
        except AttributeError:
            assert isinstance(other_start, datetime.time)
        
        try:
            other_end = other_end.time().replace(second=0)
        except AttributeError:
            assert isinstance(other_end, datetime.time)

            
        logger.debug("DURATION attempting w/ other_start and other_end: %s, %s self: %s", other_start, other_end, self)
        return self.start <= other_start and other_end <= self.end

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
    def duration(self):
        return datetime.timedelta(hours=self.end.hour - self.start.hour, minutes=self.end.minute - self.start.minute)

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


@dataclass
class Event:
    title: str
    start: datetime.datetime
    end: datetime.datetime
    description: str = None


    @property
    @cache
    def duration(self) -> Duration:
        return Duration(self.start, self.end)

    @classmethod
    def get_from_calendars(cls, start: datetime.datetime, end: datetime.datetime) -> Iterator:
        for event in get_events(start, end, collated=True):
            desc = event.event.get("DESCRIPTION")
            if desc and "the official Google Calendar app" in desc:
                desc = None
            yield cls(
                title=event.event.get("SUMMARY"), 
                description=desc, 
                start=event.event.start, end=event.event.end)


 
class TIME_OF_DAY(Enum):
    OVERNIGHT_MORNING = Duration.create(start_hour=0, end_hour=5)
    EARLY_MORNING = Duration.create(start_hour=5, end_hour=8)
    MIDMORNING = Duration.create(start_hour=5, end_hour=12)
    MORNING = Duration.create(start_hour=0, end_hour=12)
    LATE_MORNING = Duration.create(
        start_hour=10, start_minute=30, end_hour=11, end_minute=30
    )
    NOON = Duration.create(
        start_hour=11, start_minute=30, end_hour=12, end_minute=30
    )
    EARLY_AFTERNOON = Duration.create(start_hour=12, end_hour=2, end_minute=30)
    AFTERNOON = Duration.create(start_hour=12, end_hour=17)
    LATE_AFTERNOON = Duration.create(start_hour=16, end_hour=17)
    EARLY_EVENING = Duration.create(start_hour=17, end_hour=18)
    EVENING = Duration.create(start_hour=17, end_hour=20)
    LATE_EVENING = Duration.create(start_hour=19, end_hour=20)
    NIGHT = Duration.create(start_hour=20, end_hour=0)
    EVENING_AND_NIGHT = EVENING | NIGHT

    @property
    def start(self):
        return self.value.start

    @property
    def end(self):
        return self.value.end

    def __contains__(
        self, other: datetime.datetime | datetime.time | Duration
    ) -> bool:

        # If this is a task, get duration from task
        try:
            other = other.routine_time
        except AttributeError:
            pass
        try:
            other = other.time_of_day
        except AttributeError:
            pass

        else:
            return other in self.value
        try:
            return self.start <= other.start and self.end <= other.end
        except AttributeError:
            logger.exception("TIME_OF_DAY this no work: self(%s).start <= other(%s).start and self.end <= other.end", self, other)

            # either datetime or time
            try:
                # if it's datetime, make it a time
                other = other.time()
            except AttributeError:
                pass
            try:
                return self.start <= other <= self.end
            except TypeError:
                try:
                    return self.start <= other.start and other.end <= self.end
                except TypeError as exc:
                    logger.exception("TIME_OF_DAY failed: self.start(%s) <= other(%s).start and self.end(%s) <= other.end(%s)", self.start, other, self.end, other)
                    raise TypeError(f"Not comparable") from exc
            else:
                logger.debug("TIME_OF_DAY this worked: self.start(%s) <= other(%s) and self.end(%s) <= ", self.start, other, self.end)
        logger.info("TIME_OF_DAY fallback false (%s in %s)", other, self)
        return False

    def match(
        self,
        time: datetime.datetime | datetime.time,
        duration: datetime.timedelta | int = None,
    ) -> bool:

        logger.debug("checking match %s inside of %s of %s", self, duration, time)
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
            return time <= self.start or time_end > self.end
        return self.start <= time and time_end < self.end



@dataclass
class RoutineTime:
    weekdays: frozenset[int]
    time_of_day: TIME_OF_DAY | datetime.time
    weeks: frozenset[int] | None = None

    @classmethod
    def load(cls, in_dict):
        in_dict = dict(
            (k.lower(), v) for k, v in in_dict.items() if k in cls.__dataclass_fields__
        )
        if "weekdays" in in_dict:
            in_dict["weekdays"] = frozenset(in_dict["weekdays"])
        if "weeks" in in_dict:
            in_dict["weeks"] = frozenset(in_dict["weeks"])
        if "time_of_day" in in_dict:
            try:
                in_dict["time_of_day"] = TIME_OF_DAY[in_dict["time_of_day"].upper()]
            except KeyError:
                in_dict["time_of_day"] = datetime.time.fromisoformat(in_dict["time_of_day"])

        return cls(**({"weekdays": None, "weeks": None, "time_of_day": None,} | in_dict))

    def match(
        self,
        day: datetime.date | datetime.datetime | int,
        time: datetime.time | datetime.datetime | int,
        week: int = None,
        duration: datetime.timedelta | int = None,
    ) -> bool:
        if self.weekdays is None and self.weeks is None and self.time_of_day is None:
            return False
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

            if self.time_of_day is not None and not self.time_of_day.match(time, duration):
                return False
        return True



@dataclass
class Task:
    title: str
    description: str = None
    due: datetime.date | datetime.datetime = None
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
            (k.lower(), v) for k, v in in_dict.items() if k.lower() in cls.__dataclass_fields__
        )
        if "due" in in_dict:
            try:
                in_dict["due"] = datetime.date.fromisoformat(in_dict["due"])
            except ValueError:
                in_dict["due"] = datetime.datetime.fromisoformat(in_dict["due"])
        if "routine_time" in in_dict:
            in_dict["routine_time"] = RoutineTime.load(in_dict["routine_time"])
        
        loaded =  cls(**in_dict)

        return loaded

def tasks_by_routine_day_and_time(tasks: list[Task], valid_times: list[TIME_OF_DAY] = None) -> dict[int, set[Task]]:
    sorted_tasks = {}
    if valid_times is None:
        valid_times = list(TIME_OF_DAY)

    # get most specific time first
    sorted(valid_times, key=lambda x: x.value.duration())
    for task in tasks:
        if task.routine_time is None:
            continue

        elif task.routine_time.time_of_day is not None and task.routine_time.time_of_day not in valid_times:
            for valid_time in valid_times:
                if task.routine_time in valid_time:
                    time_of_day = valid_time
                    break
            else:
                raise ValueError(f"Could not find valid time for {task.routine_time} in {valid_times}")
        else:
            time_of_day = task.routine_time.time_of_day

        task_weekdays = task.routine_time.weekdays
        if task_weekdays is None:
            task_weekdays = list(range(7))

        for weekday in task_weekdays:
            sorted_tasks.setdefault(weekday, dict()).setdefault(time_of_day, list()).append(task)
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
