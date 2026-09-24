import importlib
from argparse import ArgumentParser
from collections.abc import Callable
from datetime import date, timedelta
from logging import CRITICAL, NOTSET, WARNING, getLevelNamesMapping
from pathlib import Path

import dandiscribe

importlib.reload(dandiscribe)
import dandiscribe.util

importlib.reload(dandiscribe.util)
import dandiscribe.enums

importlib.reload(dandiscribe.enums)
import dandiscribe.calendar

importlib.reload(dandiscribe.calendar)

import dandiscribe.calendar.main

importlib.reload(dandiscribe.calendar.main)


def _delta_or_date(in_str: str) -> Callable[[date], timedelta]:
    match = dandiscribe.calendar.main.TIME_DELTA_RE.match(in_str)
    factory: Callable[[date], timedelta] | None = None
    if match is not None:
        factory = dandiscribe.calendar.main.delta_from_match_helper(match)
        if factory is None:
            raise TypeError("Failed to get delta factory from CLI args")
    else:

        def factory(start: date) -> timedelta:
            return date.fromisoformat(in_str) - start

    return factory


def _default_delta_factory(start: date, delta=timedelta(days=90)) -> timedelta:
    return delta


def main():
    parser: ArgumentParser = ArgumentParser()
    _ = parser.add_argument(
        "--start", type=date.fromisoformat, default=date.today()
    )
    _ = parser.add_argument(
        "--end",
        type=_delta_or_date,
        dest="end_factory",
        default=_default_delta_factory,
    )
    _ = parser.add_argument(
        "--save_to", default=str(Path().home().joinpath("calendar.sla"))
    )
    _ = parser.add_argument(
        "--pdf", default=Path().home().joinpath("calendar.pdf")
    )
    _ = parser.add_argument(
        "--log_level",
        default="WARNING",
        choices=getLevelNamesMapping().values(),
        type=getLevelNamesMapping().get,
    )
    _ = parser.add_argument("--visual_debug", action="store_true")
    _ = parser.add_argument(
        "--debug", action="store_const", dest="log_level", const=10
    )
    interact_group = parser.add_mutually_exclusive_group()
    _ = interact_group.add_argument(
        "--non-interactive", "--NI", dest="interactive", action="store_false"
    )
    _ = interact_group.add_argument(
        "--interactive", dest="interactive", action="store_true"
    )
    parser.set_defaults(interactive=True)
    noisiness_grp = parser.add_mutually_exclusive_group()
    _ = noisiness_grp.add_argument("--verbose", "-v", action="count", default=0)
    _ = noisiness_grp.add_argument(
        "--quiet", "--quieten", "-q", action="count", default=0
    )
    parser.set_defaults(log_level=WARNING)
    select_grp = parser.add_mutually_exclusive_group()
    select_grp.add_argument("--no_master_page", "--NM", action="store_true")
    select_grp.add_argument("--no_main_draw", "--ND", action="store_true")

    parsed = parser.parse_args()
    parsed.log_level = min(
        CRITICAL,
        max(
            NOTSET,
            parsed.log_level + (parsed.quiet * 10) - (parsed.verbose * 10),
        ),
    )
    dandiscribe.calendar.main.entry_point(
        routines_file="/home/dandelion/src/toolbelt/src/dandiscribe/routines.yml",
        start=parsed.start,
        end=parsed.start + parsed.end_factory(parsed.start),
        interactive=parsed.interactive,
        log_level=parsed.log_level,
        pdf_out=parsed.pdf,
        save_to=parsed.save_to,
        close=True,
        no_master_draw=parsed.no_master_page,
        no_main_draw=parsed.no_main_draw,
        visual_debug=False,
    )


if __name__ == "__main__":
    main()
