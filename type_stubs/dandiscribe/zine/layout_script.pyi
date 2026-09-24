from _typeshed import Incomplete
from dandiscribe import script_utils as script_utils
from dandiscribe.data import Margins as Margins, Size as Size
from dandiscribe.enums import (
    InsertPaddingPages as InsertPaddingPages,
    PaperSize as PaperSize,
    Unit as Unit,
)
from dandiscribe.log import configure as configure
from dandiscribe.zine.layout import FinalDoc as FinalDoc, Layout as Layout
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import NamedTuple

TEST_SOURCE_8: Incomplete
TEST_SOURCE_12: Incomplete
TEST_SOURCE_16: Incomplete
TEST_SOURCE_8_HALF: Incomplete
TEST_SOURCE_12_HALF: Incomplete
TEST_SOURCE_16_HALF: Incomplete
MAKE_OUT_DIR: bool
TEST_OUT_DIR: Path
TEST_SOURCE_2: Traversable
TEST_SOURCE_8_EIGHTH: Traversable
TEST_SOURCE_12_LANDSCAPE: Traversable
TEST_SOURCE_16_LANDSCAPE: Traversable
LOGGER: Incomplete
DEFAULT_VIS_LOG_LEVEL: Incomplete

class TestLayout(NamedTuple):
    layout: Layout
    source: Traversable
    doc: FinalDoc
    aliases: list[str] | None = ...

TEST_HALF_DOC: FinalDoc
TEST_QUARTER_DOC: FinalDoc
TEST_QUARTER_3PG_DOC: FinalDoc
TEST_QUARTER_LANDSCAPE_DOC: FinalDoc
TEST_EIGHTH_DOC: FinalDoc
LAYOUTS: Incomplete

def test_layouts(
    keep_source_open: bool = False,
    keep_final_open: bool = False,
    paper_size: PaperSize | None = None,
    layouts: list[str] | None = None,
    pad_pages: InsertPaddingPages = ...,
    add_doc_pages: bool = False,
) -> None: ...

class NoTestsRun(Exception):
    def __init__(self) -> None: ...

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
    pad_pages: InsertPaddingPages = ...,
    add_doc_pages: bool = False,
) -> None: ...
def main() -> None: ...
