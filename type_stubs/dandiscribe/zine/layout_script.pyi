from _typeshed import Incomplete
from dandiscribe import script_utils as script_utils
from dandiscribe.data import Margins as Margins, Size as Size
from dandiscribe.enums import (
    PaperSize as PaperSize,
    Unit as Unit,
    UnitType as UnitType,
)
from dandiscribe.zine.layout import (
    FinalDoc as FinalDoc,
    HALF_DOC as HALF_DOC,
    Layout as Layout,
    LayoutVal as LayoutVal,
    QUARTER_DOC as QUARTER_DOC,
)
from enum import Enum as Enum
from importlib.resources.abc import Traversable
from numpy import test as test
from pathlib import Path
from re import U as U
from scribus import inch as inch
from typing import NamedTuple

TEST_SOURCE_8: Incomplete
TEST_SOURCE_12: Incomplete
TEST_SOURCE_16: Incomplete
TEST_SOURCE_8_HALF: Incomplete
TEST_SOURCE_12_HALF: Incomplete
TEST_SOURCE_16_HALF: Incomplete

class TestLayout(NamedTuple):
    layout: Layout
    source: Traversable
    doc: FinalDoc
    aliases: list[str] | None = ...

TEST_HALF_DOC: FinalDoc
TEST_QUARTER_DOC: FinalDoc
TEST_EIGHTH_DOC: FinalDoc
LAYOUTS: Incomplete

def test_layouts(
    keep_source_open: bool = False,
    keep_final_open: bool = False,
    paper_size: PaperSize = ...,
    layouts: list[str] | None = None,
) -> None: ...
def run_layout(
    source_file: Path,
    dest_path: Path,
    layout: Layout,
    pages: int,
    paper_size: Size,
    signature_sheets: int,
    unit: Unit = ...,
    keep_source_open: bool = False,
    keep_final_open: bool = False,
) -> None: ...
def main() -> None: ...
