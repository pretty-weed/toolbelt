from importlib.resources.abc import Traversable
from argparse import _SubParsersAction, ArgumentError, ArgumentParser, Namespace
from enum import Enum
import importlib
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
from os import getenv
from pathlib import Path
from re import U
import sys
import tempfile
import traceback
from typing import Any, NamedTuple

from dandy_lib.cli.parser import add_output_force_overwrite_to_parser
from dandy_lib.cli.enums import EnumAction

from dandiscribe import script_utils

importlib.reload(script_utils)
script_utils.reload()
from dandiscribe.log import configure
from numpy import test

LOGGER = configure(__name__)


def main() -> None:
    parent_parser: ArgumentParser = ArgumentParser(
        exit_on_error=False, add_help=False
    )
    _ = parent_parser.add_argument(
        "--keep_source_open", "--KS", action="store_true"
    )
    _ = parent_parser.add_argument(
        "--keep_final_open", "--KF", action="store_true"
    )

    parser: ArgumentParser = ArgumentParser(parents=[parent_parser])

    subparsers: _SubParsersAction[ArgumentParser] = parser.add_subparsers(
        required=True
    )
    test_parser = subparsers.add_parser("test", parents=[parent_parser])
    _ = test_parser.add_argument("layouts", nargs="*")
    _ = test_parser.add_argument("--foo", action="append", nargs="+", type=int)

    run_parser = subparsers.add_parser(name="run")
    _ = run_parser.add_argument("source", type=Path)
    _ = run_parser.add_argument("dest", nargs="?")
    _ = run_parser.add_argument("pages", type=int)

    _ = run_parser.add_argument("--signature_size", type=int, default=4)
    # add_output_force_overwrite_to_parser(run_parser)

    try:
        parsed: Namespace = parser.parse_args()
    except ArgumentError as exc:
        sys.argv.insert(1, "run")
        # parser.exit_on_error = True
        LOGGER.exception("inserting default run arg")
        parsed = parser.parse_args()
    LOGGER.debug(
        "in script %s: about to run %s(%s)",
        __name__,
        parsed,
        str(vars(parsed)),
    )
    action_kwargs: dict[str, Any] = dict(
        (k, v) for k, v in vars(parsed).items() if k != "action"
    )


if __name__ == "__main__":
    main()
