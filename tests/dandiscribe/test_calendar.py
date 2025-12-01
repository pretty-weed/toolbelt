from datetime import date, datetime, time, timedelta
from enum import Enum
import sys

import unittest
import unittest.mock as mock

import pytest

from .scribus_module_mock import ScribusSpec

# todo, setup dir of scribus
with mock.patch.dict(sys.modules, scribus=ScribusSpec):
    import dandiscribe.calendar

ALL_DAY_DURATION = dandiscribe.calendar.Duration(time(), time(23, 59, 59))
MIDNIGHT_TO_ONE_DURATION = dandiscribe.calendar.Duration(time(), time(1))
NOON_TO_18_DURATION = dandiscribe.calendar.Duration(time(12), time(18))
PM_DURATION = dandiscribe.calendar.Duration(time(12), time(23, 59, 59))


class SampleDurationEnum(Enum):
    ALL_DAY = ALL_DAY_DURATION
    MIDNIGHT_TO_ONE = MIDNIGHT_TO_ONE_DURATION
    NOON_TO_18 = NOON_TO_18_DURATION
    PM = PM_DURATION


class TestDurations(unittest.TestCase):

    def test_create(self):
        start_dt = datetime(2025, 8, 26, 3)
        end_dt = datetime(2025, 8, 26, 15)
        start_time = start_dt.time()
        end_time = end_dt.time()
        # from datetime and datetime
        res = dandiscribe.calendar.Duration.create(3, 15)
        self.assertEqual(res.start, start_time)
        self.assertEqual(res.end, end_time)

    def test_contains(self):
        midnight_time = time(0)
        three_dt = datetime(2025, 8, 26, 3)
        three_oh_one_dt = datetime(2025, 8, 26, 3, 1)
        three_time = time(3)
        three_thirty_time = time(3, 30)

        self.assertTrue(three_dt in ALL_DAY_DURATION)
        self.assertTrue(midnight_time in ALL_DAY_DURATION)
        self.assertFalse(three_oh_one_dt in NOON_TO_18_DURATION)
        self.assertFalse(three_time in NOON_TO_18_DURATION)

        self.assertTrue(SampleDurationEnum.NOON_TO_18 in PM_DURATION)

        self.assertTrue(NOON_TO_18_DURATION in PM_DURATION)
        self.assertFalse(ALL_DAY_DURATION in NOON_TO_18_DURATION)
        self.assertFalse(MIDNIGHT_TO_ONE_DURATION in NOON_TO_18_DURATION)


class TestTasks(unittest.TestCase):
    def test_tasks_by_routine_day_and_time(self):
        every_day_routine = dandiscribe.calendar.RoutineTime(
            weekdays=None,
            time_of_day=dandiscribe.calendar.TIME_OF_DAY.AFTERNOON,
        )
        every_day_task = dandiscribe.calendar.Task(
            title="edt", routine_time=every_day_routine
        )
        daily_res = {
            dandiscribe.calendar.TIME_OF_DAY.AFTERNOON: [every_day_task]
        }
        self.assertEqual(
            dandiscribe.calendar.tasks_by_routine_day_and_time(
                [every_day_task]
            ),
            dict((i, daily_res) for i in range(7)),
        )

        with self.subTest("mwf-morning"):
            mwf_am_routine = dandiscribe.calendar.RoutineTime(
                weekdays=frozenset([0, 2, 4]),
                time_of_day=dandiscribe.calendar.TIME_OF_DAY.MORNING,
            )
            mwf_am_task = dandiscribe.calendar.Task(
                title="mwf-am", routine_time=mwf_am_routine
            )
            res_dict = {dandiscribe.calendar.TIME_OF_DAY.MORNING: [mwf_am_task]}

            self.assertEqual(
                dandiscribe.calendar.tasks_by_routine_day_and_time(
                    [mwf_am_task]
                ),
                dict((i, res_dict) for i in [0, 2, 4]),
            )


class TestData(unittest.TestCase):
    def test_setup(self):

        cal_events = dandiscribe.calendar.Event.get_from_calendars(
            datetime.combine(date.today(), time.min),
            datetime.combine(date.today() + timedelta(weeks=1), time.max),
        )

        print(cal_events)
