from importlib.resources.abc import Traversable


from argparse import _SubParsersAction, ArgumentError, ArgumentParser, Namespace
from enum import Enum
import importlib
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
import logging
from os import getenv
from pathlib import Path
from re import U
import sys
import tempfile
import traceback
from typing import Any, NamedTuple

from dandy_lib.cli.parser import add_output_force_overwrite_to_parser
from dandy_lib.cli.enums import EnumAction

from numpy import test
from scribus import inch


from dandiscribe import script_utils

importlib.reload(script_utils)
script_utils.reload()
import dandiscribe
from dandiscribe.zine import layout as zine_layout
from dandiscribe.data import Margins, Size
from dandiscribe.zine.layout import (
    FinalDoc,
    Layout,
    LayoutVal,
    QUARTER_DOC,
    HALF_DOC,
)
from dandiscribe.enums import InsertPaddingPages, PaperSize, Unit, UnitType
from dandiscribe.log import configure


MAKE_OUT_DIR: bool = getenv("MAKE_TEST_ZINE_DIR", "").lower() in [
    "t",
    "true",
    "y",
    "yes",
    "1",
]
TEST_OUT_DIR: Path = Path(
    getenv("TEST_ZINE_OUT_DIR", str(Path().home().joinpath("zines", "test")))
)
if MAKE_OUT_DIR and not TEST_OUT_DIR.exists():
    TEST_OUT_DIR.mkdir(parents=True)


def _source_helper(num_pages: int, aspect_ratio: str = "") -> Traversable:
    return files("dandiscribe.source_files").joinpath(
        f"test_pages-{num_pages}{'-' + aspect_ratio if aspect_ratio else ''}.sla"
    )


# test_pages-n.sla has n pages, including front and back cover.
TEST_SOURCE_2: Traversable = _source_helper(
    2,
)
TEST_SOURCE_8: Traversable = _source_helper(
    8,
)
TEST_SOURCE_12: Traversable = _source_helper(
    12,
)
TEST_SOURCE_16: Traversable = _source_helper(
    16,
)
TEST_SOURCE_8_EIGHTH: Traversable = _source_helper(8, "eighth")
TEST_SOURCE_8_HALF: Traversable = _source_helper(8, "half")
TEST_SOURCE_12_HALF: Traversable = _source_helper(12, "half")
TEST_SOURCE_12_LANDSCAPE: Traversable = _source_helper(12, "landscape")
TEST_SOURCE_16_LANDSCAPE: Traversable = _source_helper(16, "landscape")

LOGGER = configure(__name__)

DEFAULT_VIS_LOG_LEVEL = logging.ERROR


class TestLayout(NamedTuple):
    layout: Layout
    source: Traversable
    doc: FinalDoc
    aliases: list[str] | None = None


def _test_out_path(name: str) -> str:
    return str(TEST_OUT_DIR.joinpath(name))


TEST_HALF_DOC: FinalDoc = FinalDoc(
    _test_out_path("test_res_half.sla"), 4, zine_layout.Layout.HALF
)
TEST_QUARTER_DOC: FinalDoc = FinalDoc(
    _test_out_path("test_res_quarter.sla"),
    4,
    zine_layout.Layout.QUARTER_PORTRAIT,
)
TEST_QUARTER_3PG_DOC: FinalDoc = FinalDoc(
    _test_out_path("test_res_quarter_3pg.sla"),
    3,
    Layout.QUARTER,
)
TEST_QUARTER_LANDSCAPE_DOC: FinalDoc = FinalDoc(
    _test_out_path("test_res_quarter_landscape.sla"),
    4,
    zine_layout.Layout.QUARTER_LANDSCAPE,
)
TEST_EIGHTH_DOC: FinalDoc = FinalDoc(
    _test_out_path("test_res_eight.sla"),
    1,
    zine_layout.Layout.EIGHT_PAGE_MINI,
)

LAYOUTS = {
    Layout.HALF.name: TestLayout(
        Layout.HALF, TEST_SOURCE_8_HALF, TEST_HALF_DOC, aliases=["2", "1/2"]
    ),
    Layout.QUARTER.name: TestLayout(
        Layout.QUARTER, TEST_SOURCE_16, TEST_QUARTER_DOC, aliases=["4", "1/4"]
    ),
    "QUARTER_WRONG_LAYOUT": TestLayout(
        Layout.QUARTER, TEST_SOURCE_2, TEST_QUARTER_DOC, aliases=["QRL"]
    ),
    "QUARTER_WRONG_PGNUM": TestLayout(
        Layout.QUARTER, TEST_SOURCE_16, TEST_QUARTER_3PG_DOC, aliases=["QRP"]
    ),
    "QUARTER_LANDSCAPE": TestLayout(
        Layout.QUARTER,
        TEST_SOURCE_16_LANDSCAPE,
        doc=TEST_QUARTER_LANDSCAPE_DOC,
        aliases=["4H", "4L"],
    ),
    Layout.EIGHT_PAGE_MINI.name: TestLayout(
        Layout.EIGHT_PAGE_MINI,
        TEST_SOURCE_8_EIGHTH,
        TEST_EIGHTH_DOC,
        aliases=["eight", "eighth", "8", "1/8", "mini"],
    ),
}


def test_layouts(
    keep_source_open: bool = False,
    keep_final_open: bool = False,
    paper_size: PaperSize | None = None,
    layouts: list[str] | None = None,
    pad_pages: InsertPaddingPages = InsertPaddingPages.NO,
    add_doc_pages: bool = False,
) -> None:

    if layouts is None or not layouts:
        print("Testing all layouts")
        layouts = list(LAYOUTS)
    tested: bool = False
    for do_layout in layouts:

        for name, test_layout in LAYOUTS.items():
            if paper_size is None:
                test_paper = test_layout.doc.print_page_size
            else:
                test_paper = paper_size
            if not (
                name.upper() == do_layout.upper()
                or any(
                    do_layout.lower() == a.lower()
                    for a in (test_layout.aliases or [])
                )
            ):
                continue

            with as_file(test_layout.source) as source_file:

                run_layout(
                    source_file,
                    Path(test_layout.doc.name),
                    test_layout.layout,
                    test_layout.doc.pages,
                    test_paper,
                    test_layout.doc.signature_sheets,
                    test_layout.doc.unit,
                    keep_source_open,
                    keep_final_open,
                    pad_pages,
                )

            tested = True

    if not tested:
        LOGGER.error("No Tests were run!")
        raise NoTestsRun()


class NoTestsRun(Exception):
    def __init__(self):
        super().__init__("No tests were run!")


def run_layout(
    source_file: Path,
    dest_path: Path,
    layout: Layout,
    pages: int,
    paper_size: Size,
    signature_sheets: int,
    unit: Unit = Unit.INCHES,
    keep_source_open: bool = False,
    keep_final_open: bool = False,
    pad_pages: InsertPaddingPages = InsertPaddingPages.NO,
    add_doc_pages: bool = False,
) -> None:

    # zine_layout.create_from_current_doc(zine_layout.Layout.QUARTER)
    close_source = not keep_source_open
    close_final = not keep_final_open
    # ToDo Make margins configurable in cli
    doc = FinalDoc(
        str(dest_path),
        pages,
        layout,
        signature_sheets,
        paper_size,
        unit,
        Margins(*([0.5] * 4)),
    )
    doc.assemble(
        source_file,
        close_source,
        close_final,
        insert_padding_pages=pad_pages,
        insert_doc_pages=add_doc_pages,
    )


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
    _ = parent_parser.add_argument(
        "--paper_size",
        choices=PaperSize,
        type=PaperSize,
        action=EnumAction,
        default=PaperSize.LETTER,
    )
    _ = parent_parser.add_argument(
        "--pad_pages",
        choices=InsertPaddingPages,
        action=EnumAction,
        default=InsertPaddingPages.NO,
    )
    _ = parent_parser.add_argument("--add_doc_pages", action="store_true")
    # divide log level / 10 as we want a count
    _ = parent_parser.add_argument(
        "--visual_debug", "-V", "--VD", action="count"
    )
    parser: ArgumentParser = ArgumentParser(parents=[parent_parser])

    subparsers: _SubParsersAction[ArgumentParser] = parser.add_subparsers(
        required=True
    )
    test_parser = subparsers.add_parser("test", parents=[parent_parser])
    test_parser.set_defaults(action=test_layouts)
    _ = test_parser.add_argument("layouts", nargs="*")

    run_parser = subparsers.add_parser(name="run")
    run_parser.set_defaults(action=run_layout)
    _ = run_parser.add_argument("source", type=Path)
    _ = run_parser.add_argument("dest", nargs="?")
    _ = run_parser.add_argument("pages", type=int)
    _ = run_parser.add_argument(
        "--unit",
        choices=Unit,
        type=Unit,
        action=EnumAction,
        default=Unit.INCHES,
    )
    _ = run_parser.add_argument(
        "--layout",
        choices=Layout,
        type=Layout,
        action=EnumAction,
        required=True,
    )
    _ = run_parser.add_argument("--signature_size", type=int, default=4)
    # add_output_force_overwrite_to_parser(run_parser)
    parser.set_defaults(action=run_layout)
    try:
        parsed: Namespace = parser.parse_args()
    except ArgumentError as exc:
        sys.argv.insert(1, "run")
        # parser.exit_on_error = True
        LOGGER.exception("inserting default run arg")
        parsed = parser.parse_args()
    LOGGER.debug(
        "in script %s: about to run %s(%s) [%s]",
        __name__,
        parsed.action,
        str(vars(parsed)),
        parsed,
    )
    if parsed.visual_debug:
        new_level = DEFAULT_VIS_LOG_LEVEL - (parsed.visual_debug * 10)
        dandiscribe.VISUAL_DEBUG_LEVEL = new_level

    action_kwargs: dict[str, Any] = dict(
        (k, v)
        for k, v in vars(parsed).items()
        if k not in ["action", "visual_debug"]
    )
    try:
        parsed.action(**action_kwargs)
    except Exception as exc:
        print(exc, flush=True)
        LOGGER.exception(
            "Exception Raised:\n%s\n\nkwargs:%s",
            traceback.format_exc(),
            action_kwargs,
        )
        raise exc


if __name__ == "__main__":
    main()
