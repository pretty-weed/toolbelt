# get events from calendar url

import calendar
from collections.abc import Container, Iterator
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum, EnumMeta, IntEnum
from functools import cache
from logging import INFO, getLogger
from os import getenv
from pathlib import Path
from typing import Any, NamedTuple, Self, TypeAlias, cast

import icalendar
from requests import get
from requests.exceptions import ConnectionError
from yaml import safe_load

CONF_FILE = Path(
    getenv("CONF_FILE", Path().home().joinpath(".private", "calendars.yaml"))
)
logger = getLogger(__name__)
logger.setLevel(INFO)


class CalEvent(NamedTuple):
    calendar: icalendar.Calendar
    event: icalendar.Event


def get_conf(filepath: Path = CONF_FILE) -> dict[str, Any]:
    if not CONF_FILE.exists() or not CONF_FILE.read_text():
        return {}

    return safe_load(CONF_FILE.read_text())


def get_calendars(
    calendar_name: str | None = None,
) -> dict[str, icalendar.Calendar]:
    calendars: dict[str, icalendar.Calendar] = {}
    for calendar, url in get_conf().get("external_calendars", {}).items():
        if calendar_name is not None and calendar != calendar_name:
            continue
        try:
            res = get(url)
        except ConnectionError:
            logger.exception("Failed to get calendar")
        else:
            calendars[calendar] = icalendar.Calendar.from_ical(res.text)  # type: ignore[assignment]
            # ToDo maybe assert this is actually a calendar
    return calendars


def _date_and_dt_key(
    in_val: date | datetime,
) -> datetime:
    try:
        return datetime.combine(in_val.date(), in_val.time())  # type: ignore[union-attr]
    except AttributeError:
        # in_val is date
        return datetime.combine(in_val, time.min)


def get_events(
    start: date,
    end: date,
    collated: bool = True,
    calendar_name: str | None = None,
) -> Iterator[CalEvent]:

    if collated:
        events: list[CalEvent] = []
    for calendar in get_calendars(calendar_name).values():
        if collated:
            events.extend(
                CalEvent(calendar, event) for event in calendar.events
            )
        else:
            for event in calendar.events:
                # force start to a datetime
                yield CalEvent(calendar, event)

    if collated:

        yield from sorted(
            events, key=lambda cv: _date_and_dt_key(cv.event.start)
        )


class CMP_VALUE(IntEnum):
    EQUAL = 0
    SUBSET = -1
    SUPERSET = 1
    LESS_THAN_INTERSECTION = -2
    LTI = -2
    GREATER_THAN_INTERSECTION = 2
    GTI = 2
    LESS_THAN = -3
    LT = -3  # Neither is sub/superset
    GREATER_THAN = 3
    GT = 3  # Neither is sub/superset


AW_YEAR = 1900
AW_MONTH = 1


class WeekdayMeta(EnumMeta):
    @property
    def members(cls) -> dict[datetime, AbstractWeekday]:
        """A true class-level property wrapping the map."""
        return cast(dict[datetime, AbstractWeekday], cls._value2member_map_)


class AbstractWeekday(datetime, Enum, metaclass=WeekdayMeta):
    """
    An abstract weekday Enum using January 1900 as a base.
    January 1st, 1900 was a Monday.
    """

    MONDAY = (AW_YEAR, AW_MONTH, 1)
    TUESDAY = (AW_YEAR, AW_MONTH, 2)
    WEDNESDAY = (AW_YEAR, AW_MONTH, 3)
    THURSDAY = (AW_YEAR, AW_MONTH, 4)
    FRIDAY = (AW_YEAR, AW_MONTH, 5)
    SATURDAY = (AW_YEAR, AW_MONTH, 6)
    SUNDAY = (AW_YEAR, AW_MONTH, 7)

    def at_time(self, hour: int, minute: int = 0) -> datetime:
        """Combines this abstract day with a specific time of day."""
        return datetime(self.year, self.month, self.day, hour, minute)

    @classmethod
    def current(cls) -> Self:
        now = datetime.now()
        now_idx = datetime(year=AW_YEAR, month=AW_YEAR, day=1 + now.weekday())

    def next(self, start: datetime | None) -> Self:
        start = start or datetime.now()


Value2MemberMap: TypeAlias = dict[datetime, AbstractWeekday]


type Timey = time | datetime


class Duration(NamedTuple):
    start: time | datetime
    end: time | datetime

    @property
    def absolute(self) -> bool:
        match (self.start, self.end):
            case (datetime(), datetime()):
                return True
            case _:
                return False

    def cmp(self, other: Self) -> CMP_VALUE:
        if self.absolute != other.absolute:
            raise Incomaprable(self, other)
        if self == other:
            return CMP_VALUE.EQUAL
        if self.end < other.start:
            return CMP_VALUE.LT

        if self.start < other.start and other.start < self.end < other.end:
            return CMP_VALUE.LTI

        if self.start > other.end:
            return CMP_VALUE.GT

        if other.start < self.start < other.end and self.end > other.end:
            return CMP_VALUE.GTI

        assert (
            False
        ), "This should never happen, all should be caught by the above ifs"

    def __contains__(self, other: object) -> bool:

        try:
            other: time | datetime = other.value  # type: ignore[override]
        except AttributeError:
            pass
        else:
            try:
                # Deal with other as routinetime
                other_tod = other.time_of_day
            except AttributeError:
                # deal with other as either duration, time of day, datetime, or time
                try:
                    # deal with other as duration or time of day
                    # these should be datetime or time
                    other_start: Timey = other.start
                    other_end: Timey = other.end
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
            assert isinstance(other_start, time)

        try:
            other_end = other_end.time().replace(second=0)
        except AttributeError:
            assert isinstance(other_end, time)

        logger.debug(
            "DURATION attempting w/ other_start and other_end: %s, %s self: %s",
            other_start,
            other_end,
            self,
        )
        return self.start <= other_start and other_end <= self.end

    def __and__(self, other: Self) -> Duration:
        print(f"self & other: {self} & {other}")
        early, late = sorted([self, other], key=lambda x: x.start)
        if early.end < late.start:
            raise ValueError(f"NO NO NO {early} & {late} ({self} & {other})")
            return

        res = Duration(max(early.start, late.start), min(early.end, late.end))

        print(f"{self} & {other} = {res}")
        return res

    def __or__(self, other) -> Duration | None:
        early, late = sorted([self, other], key=lambda x: x.start)
        print(f"self | other: {self} | {other}")
        if early.end < late.start:
            print(
                f"early, late: {early}, {late}; self | other: {self}, {other}"
            )
            # disjoint
            return None

        res = Duration(min(early.start, late.start), max(early.end, late.end))

        print(f"{self} | {other} = {res}")

        return res

    def duration(self):
        return timedelta(
            hours=self.end.hour - self.start.hour,
            minutes=self.end.minute - self.start.minute,
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
            time(start_hour, start_minute),
            time(end_hour, end_minute),
        )


@dataclass
class Event:
    title: str
    start: datetime
    end: datetime
    description: str = None

    @property
    @cache
    def duration(self) -> Duration:
        return Duration(self.start, self.end)

    @classmethod
    def get_from_calendars(
        cls, start: datetime, end: datetime
    ) -> Iterator[Self]:
        for event in get_events(start, end, collated=True):
            desc = event.event.get("DESCRIPTION")
            if desc and "the official Google Calendar app" in desc:
                desc = None
            yield cls(
                title=event.event.get("SUMMARY"),
                description=desc,
                start=event.event.start,
                end=event.event.end,
            )


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
    ALL_DAY = ((MORNING | AFTERNOON) | EVENING) | NIGHT

    @property
    def start(self):
        return self.value.start

    @property
    def end(self):
        return self.value.end

    def __contains__(self, other: datetime | time | Duration) -> bool:

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
            logger.exception(
                "TIME_OF_DAY this no work: self(%s).start <= other(%s).start and self.end <= other.end",
                self,
                other,
            )

            # either datetime or time
            try:
                # if it's datetime, make it a time
                other = other.time()
            except AttributeError:
                pass
            try:
                res: bool = self.start <= other <= self.end
            except TypeError:
                try:
                    return self.start <= other.start and other.end <= self.end
                except TypeError as exc:
                    logger.exception(
                        "TIME_OF_DAY failed: self.start(%s) <= other(%s).start and self.end(%s) <= other.end(%s)",
                        self.start,
                        other,
                        self.end,
                        other,
                    )
                    raise TypeError("Not comparable") from exc
            else:
                logger.debug(
                    "TIME_OF_DAY this worked: self.start(%s) <= other(%s) and self.end(%s) <= ",
                    self.start,
                    other,
                    self.end,
                )
                return res
        logger.info("TIME_OF_DAY fallback false (%s in %s)", other, self)
        return False

    def match(
        self,
        time: datetime | time,
        duration: timedelta | int | None = None,
    ) -> bool:

        logger.debug(
            "checking match %s inside of %s of %s", self, duration, time
        )
        try:
            # this will work for datetime
            time = time.time()
        except AttributeError:
            # excepted for datetime, treat time as a `time()`
            pass

        if duration is None:
            time_end = time
        else:
            try:
                time_end = time + duration
            except TypeError:
                # an int
                time_end = time + timedelta(hours=duration)

        # Start is after end, is overnight
        if self.start > self.end:
            return time <= self.start or time_end > self.end
        return self.start <= time and time_end < self.end


class RoutineTime(NamedTuple):
    weekdays: frozenset[int] | None
    time_of_day: TIME_OF_DAY | time | None
    weeks: frozenset[int] | None = None
    start: date | None = None
    end: date | None = None

    @classmethod
    def load(cls, in_dict):
        in_dict = dict(
            (k.lower(), v) for k, v in in_dict.items() if k in cls._fields
        )
        if "weekdays" in in_dict:
            in_dict["weekdays"] = frozenset(int(v) for v in in_dict["weekdays"])
        if "weeks" in in_dict:
            in_dict["weeks"] = frozenset(int(v) for v in in_dict["weeks"])
        if "time_of_day" in in_dict:
            try:
                in_dict["time_of_day"] = TIME_OF_DAY[
                    in_dict["time_of_day"].upper()
                ]
            except KeyError:
                in_dict["time_of_day"] = time.fromisoformat(
                    in_dict["time_of_day"]
                )

        for param in ["start", "end"]:
            if param in in_dict:
                in_dict[param] = date.fromisoformat(in_dict[param])

        return cls(
            **(
                {
                    "weekdays": None,
                    "weeks": None,
                    "time_of_day": None,
                }
                | in_dict
            )
        )

    def match(
        self,
        day: date | datetime | int,
        time: time | datetime | int,
        week: Optional[int] = None,
        duration: Optional[timedelta | int] = None,
    ) -> bool:
        if (
            self.weekdays is None
            and self.weeks is None
            and self.time_of_day is None
        ):
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
                    time = time(hour=time)
                except TypeError:
                    # time is a time, presumably
                    pass

            if duration is not None:
                try:
                    duration = timedelta(hours=duration)
                except TypeError:
                    # duration is already a delta
                    pass

            if self.time_of_day is not None and not self.time_of_day.match(
                time, duration
            ):
                return False
        return True


@dataclass
class Task(Container):
    title: str
    description: str | None = None
    due: date | datetime | None = None
    routine_time: RoutineTime | None = None

    @property
    def start_date(self) -> date | None:
        if self.routine_time is not None:
            return self.routine_time.start

        # Assumes self.due is set, per __post_init__
        try:
            return cast(datetime, self.due).date()
        except AttributeError:
            return cast(date, self.due)

    @property
    def end_date(self) -> date | None:
        if self.routine_time is not None:
            return self.routine_time.end

        try:
            return cast(datetime, self.due).date()
        except AttributeError:
            return cast(date, self.due)

    def __post_init__(self):
        if self.due is None and self.routine_time is None:
            raise TypeError("either due or routine time must not be None")
        elif self.due is not None and self.routine_time is not None:
            raise TypeError(
                "routine time and due may not both be set on a Task"
            )

    def timey_range(self) -> tuple[Timey, Timey]:
        if self.due is not None:
            try:
                self.due.date()
            except AttributeError:
                due = datetime.combine(self.due, time.min)
                return due, due
            else:
                # Above confirms that self.due is a datetime (providing client
                # code uses correct types at all)
                return self.due, self.due

    def __contains__(self, item: object) -> bool:
        return timey_cmp(self, item) in [CMP_VALUE.EQUAL, CMP_VALUE.SUPERSET]

    @classmethod
    def load(cls, in_dict):
        in_dict = dict(
            (k.lower(), v)
            for k, v in in_dict.items()
            if k.lower() in cls.__dataclass_fields__
        )
        if "due" in in_dict:
            try:
                in_dict["due"] = date.fromisoformat(in_dict["due"])
            except ValueError:
                in_dict["due"] = datetime.fromisoformat(in_dict["due"])
        if "routine_time" in in_dict:
            in_dict["routine_time"] = RoutineTime.load(in_dict["routine_time"])

        loaded = cls(**in_dict)

        return loaded


type AllTimey = Timey | Task | Duration | Event | RoutineTime | TIME_OF_DAY


class NotTimey(BaseException):
    def __init__(self, not_timey) -> None:
        super().__init__(f"{not_timey} ({type({not_timey})}) is not Timey")


def timey_get_duration(t: AllTimey) -> Duration:
    match t:
        case time() | datetime():
            return Duration(t, t)
        case Task():
            return Duration(*t.timey_range())
        case Duration():
            return t
        case TIME_OF_DAY():
            return Duration(t.start, t.end)
        case RoutineTime():
            return Duration(t.time_of_day.start, t.time_of_day.end)
        case _:
            raise NotTimey(t)


def timey_cmp(a: AllTimey, b: AllTimey) -> CMP_VALUE:
    """
    not a traditional cmp, as it also checks superset/subset.
     see CMP_VALUE for return meanings (-2->2)
    """
    # Extract the durations to compare
    ad: Duration = timey_get_duration(a)
    bd: Duration = timey_get_duration(b)
    return ad.cmp(bd)


def tasks_by_routine_day_and_time(
    tasks: list[Task], valid_times: list[TIME_OF_DAY] | None = None
) -> dict[int, dict[TIME_OF_DAY, list[Task]]]:
    sorted_tasks: dict[int, dict[TIME_OF_DAY, list[Task]]] = {}
    if valid_times is None:
        valid_times = list(TIME_OF_DAY)

    # get most specific time first
    sorted(valid_times, key=lambda x: x.value.duration())
    for task in tasks:
        if task.routine_time is None:
            continue

        elif (
            task.routine_time.time_of_day is not None
            and task.routine_time.time_of_day not in valid_times
        ):
            for valid_time in valid_times:
                # Checking for `time()` in `TIME_OF_DAY`
                if task.routine_time in valid_time:
                    time_of_day = valid_time
                    break
            else:
                raise ValueError(
                    f"Could not find valid time for {task.routine_time} in {valid_times}"
                )
        else:
            time_of_day = task.routine_time.time_of_day

        task_weekdays: frozenset[int] | None = task.routine_time.weekdays
        if task_weekdays is None:
            task_weekdays = frozenset(range(7))

        for weekday in task_weekdays:
            sorted_tasks.setdefault(weekday, dict()).setdefault(
                time_of_day, list()
            ).append(task)
    return sorted_tasks


def get_tasks(
    tasks: list[Task],
    date: date,
    time_of_day: TIME_OF_DAY | None = None,
    remove_routine: bool = False,
) -> Iterator[Task]:
    if remove_routine:
        tasks = [task for task in tasks if not task.routine_time]
    for task in tasks:
        if (task.start is not None and task.start > date) or (
            task.end is not None and task.end < date
        ):
            continue
        if task.day == date.weekday() and (
            (time_of_day is None) or (task in time_of_day)
        ):
            yield task


def get_month_tasks(
    tasks: list[Task], date: date, remove_routine: bool = True
) -> Iterator[Task]:
    # TODO get previous month tasks on calendar (back to prev monday)
    dow, last_day = calendar.monthrange(date.year, date.month)
    for day in range(1, last_day + 1):

        yield from get_tasks(
            tasks, date.replace(day=day), remove_routine=remove_routine
        )
        dow = (dow + 1) % 7


class Incomaprable(BaseException):
    def __init__(self, a, b):
        return super().__init__(f"cannot compare {a} and {b}")
