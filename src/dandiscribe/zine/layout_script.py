from argparse import _SubParsersAction, ArgumentError, ArgumentParser, Namespace
from enum import Enum
import importlib
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
from pathlib import Path
from re import U
import sys
import tempfile
from typing import NamedTuple

from dandy_lib.cli.parser import add_output_force_overwrite_to_parser
from dandy_lib.cli.enums import EnumAction

from numpy import test
from scribus import inch

# test_pages-n.sla has n pages, including front and back cover.
TEST_SOURCE_8 = files("dandiscribe.source_files").joinpath("test_pages-8.sla")
TEST_SOURCE_12 = files("dandiscribe.source_files").joinpath("test_pages-12.sla")
TEST_SOURCE_16 = files("dandiscribe.source_files").joinpath("test_pages-16.sla")

TEST_SOURCE_8_HALF = files("dandiscribe.source_files").joinpath(
    "test_pages-8-half.sla"
)
TEST_SOURCE_12_HALF = files("dandiscribe.source_files").joinpath(
    "test_pages-12.sla"
)
TEST_SOURCE_16_HALF = files("dandiscribe.source_files").joinpath(
    "test_pages-16.sla"
)

if "/usr/share/scribus/scripts" not in sys.path:
    sys.path.append("/usr/share/scribus/scripts")
from dandiscribe import script_utils

importlib.reload(script_utils)
script_utils.reload()
from dandiscribe.zine import layout as zine_layout
from dandiscribe.data import Margins, Size
from dandiscribe.zine.layout import (
    FinalDoc,
    Layout,
    LayoutVal,
    QUARTER_DOC,
    HALF_DOC,
)
from dandiscribe.enums import PaperSize, Unit, UnitType


class TestLayout(NamedTuple):
    layout: Layout
    source: Traversable
    doc: FinalDoc
    aliases: list[str] | None = None


TEST_HALF_DOC: FinalDoc = FinalDoc(
    "/home/dandelion/zines/test_res_half.sla", 4, zine_layout.Layout.HALF
)
TEST_QUARTER_DOC: FinalDoc = FinalDoc(
    "/home/dandelion/zines/test_res_quarter.sla", 4, zine_layout.Layout.QUARTER
)
TEST_EIGHTH_DOC: FinalDoc = FinalDoc(
    "/home/dandelion/zines/test_res_eight.sla",
    4,
    zine_layout.Layout.EIGHT_PAGE_MINI,
)

LAYOUTS = {
    Layout.HALF.name: TestLayout(
        Layout.HALF, TEST_SOURCE_8_HALF, TEST_HALF_DOC, aliases=["2", "1/2"]
    ),
    Layout.QUARTER.name: TestLayout(
        Layout.HALF, TEST_SOURCE_12, TEST_QUARTER_DOC, aliases=["4", "1/4"]
    ),
    Layout.EIGHT_PAGE_MINI.name: TestLayout(
        Layout.HALF,
        TEST_SOURCE_16,
        TEST_EIGHTH_DOC,
        aliases=["eight", "eighth", "8", "1/8", "mini"],
    ),
}


def test_layouts(
    keep_source_open: bool = False,
    keep_final_open: bool = False,
    paper_size: PaperSize = PaperSize.LETTER,
    layouts: list[str] | None = None,
) -> None:

    if not layouts:
        print("Testing all layouts")
        layouts: list[str] = list(LAYOUTS)

    for do_layout in layouts:
        for name, test_layout in LAYOUTS.items():
            if not (
                name.upper() == do_layout.upper()
                or any(
                    do_layout.lower() == a.lower() for a in test_layout.aliases
                )
            ):
                continue

            with as_file(test_layout.source) as source_file:

                run_layout(
                    source_file,
                    Path(test_layout.doc.name),
                    test_layout.layout,
                    test_layout.doc.pages,
                    test_layout.doc.print_page_size,
                    test_layout.doc.signature_sheets,
                    test_layout.doc.unit,
                    keep_source_open,
                    keep_final_open,
                )


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
    doc.assemble(source_file, close_source, close_final)


def main() -> None:
    parser = ArgumentParser(exit_on_error=False)
    _ = parser.add_argument("--keep_source_open", "--KS", action="store_true")
    _ = parser.add_argument("--keep_final_open", "--KF", action="store_true")
    _ = parser.add_argument(
        "--paper_size",
        choices=PaperSize,
        type=PaperSize,
        action=EnumAction,
        default=PaperSize.LETTER,
    )

    subparsers: _SubParsersAction[ArgumentParser] = parser.add_subparsers(
        required=True
    )
    test_parser = subparsers.add_parser("test")
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
    add_output_force_overwrite_to_parser(run_parser)

    parser.set_defaults(action=run_layout)
    try:
        parsed: Namespace = parser.parse_args()
    except ArgumentError as exc:
        sys.argv.insert(1, "run")
        # parser.exit_on_error = True
        parsed = parser.parse_args()

    parsed.action(
        **dict((k, v) for k, v in vars(parsed).items() if k != "action")
    )


if __name__ == "__main__":
    main()
