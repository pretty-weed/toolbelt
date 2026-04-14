import scribus
from _typeshed import Incomplete
from collections.abc import Sequence
from dandiscribe.data import Margins as Margins, Rect as Rect, Size as Size
from dandiscribe.enums import PAGESIDE as PAGESIDE, Unit as Unit
from dandiscribe.exceptions import (
    NewDocError as NewDocError,
    NoObjects as NoObjects,
)
from dandiscribe.layout import (
    Document as Document,
    PAPER_LETTER as PAPER_LETTER,
    Page as Page,
)
from dandiscribe.util import (
    CopyDest as CopyDest,
    CopySrc as CopySrc,
    copy_items as copy_items,
)
from dandy_lib.annotations import DivisibleBy as DivisibleBy
from dandy_lib.cli.enums import ChoiceEnumMeta, ChoiceEnumMixin
from dandy_lib.datatypes.tuples import MixableNamedTuple
from enum import Enum, IntEnum as IntEnum
from functools import lru_cache, partial
from pathlib import Path
from typing import Annotated, NamedTuple

LOG_DIR: Incomplete
LOG_FILE: Incomplete
LOGGER: Incomplete

def default_suffixer(filename: str | Path) -> Path: ...

class LayoutVal:
    val: int
    rows: int
    cols: int
    orientation: int
    def __init__(
        self, val: int, rows: int, cols: int, orientation: int = ...
    ) -> None: ...
    def __int__(self) -> int: ...
    def get_enum_tuple(self) -> tuple[int, int, int, int]: ...

class Layout(ChoiceEnumMixin, LayoutVal, Enum, metaclass=ChoiceEnumMeta):
    EIGHT_PAGE_MINI = (8, 2, 4)
    QUARTER = (4, 2, 2)
    HALF = (2, 1, 2)
    def __mul__(self, other) -> int: ...
    def __add__(self, other) -> int: ...
    def __floordiv__(self, other) -> int: ...
    def __rfloordiv__(self, other) -> int: ...

class PrintPage(MixableNamedTuple, Page):
    layout: Layout
    is_master: bool
    master_page: Incomplete
    source_pages: tuple["FinalSheetSpread", ...]

class SourcePage(Page): ...

class FinalSheetSpread(NamedTuple):
    left: int
    right: int
    def translate(
        self,
        source: str,
        dest_page: PrintPage,
        rect: Rect,
        dest_doc: str | None = None,
        source_rect: Rect | None = None,
        debug_rects: bool = True,
    ) -> tuple[str | None, str | None]: ...

class FinalSheet(NamedTuple):
    outside: FinalSheetSpread
    inside: FinalSheetSpread

class FinalPageSource(Enum):
    FRONT_START = ...
    FRONT_END = ...
    BACK_START = ...
    BACK_END = ...

class TranslatePosition(NamedTuple):
    page: int
    position: int

def get_signature_pages(
    page_count: int, signature_sheets: int = 1
) -> list[tuple[int, ...]]: ...
def front_back_from_signature(signature: Sequence[int]) -> list[FinalSheet]: ...

class FinalDoc(NamedTuple):
    name: str
    pages: int
    layout: Layout
    signature_sheets: int = ...
    print_page_size: Size = ...
    unit: Unit = ...
    margins: Margins = ...
    @property
    @lru_cache
    def page_size(self) -> Size: ...
    @property
    @lru_cache
    def page_usable_size(self) -> Size: ...
    @property
    @lru_cache
    def page_usable_size_pt(self) -> Size: ...
    @property
    @lru_cache
    def signatures(self) -> int: ...
    @property
    @lru_cache
    def cols(self) -> int: ...
    @property
    @lru_cache
    def spread_cols(self) -> int: ...
    @property
    @lru_cache
    def rows(self) -> int: ...
    def export_pdf(
        self,
        options: scribus.PDFfile | None = None,
        path: str | Path | None = None,
    ) -> bool: ...
    @property
    @lru_cache
    def signature_pages(self) -> list[tuple[int, ...]]: ...
    @property
    @lru_cache
    def print_pages(self) -> list[PrintPage]: ...
    def assemble(
        self,
        source: str | Path | None = None,
        close_source: bool = True,
        close_final: bool = True,
        inside_margins: bool = False,
    ): ...

HALF_DOC: partial[FinalDoc]
QUARTER_DOC: partial[FinalDoc]

def generate_pages(
    total_pages: int,
    signature_size: Annotated[int, None] = 4,
    pad: bool = False,
    has_cover: bool = True,
    has_title_page: bool = False,
    has_toc: bool = True,
    start_side: PAGESIDE = ...,
    offset_start: int = 0,
    print_size: Size = ...,
    layout: Layout = ...,
) -> None: ...
def get_page_and_pos(
    source_page: int, total_pages: int, Layout: Layout, signature_size: int = 1
) -> TranslatePosition: ...
def create_from_current_doc(
    layout: Layout,
    signature_sheets: int = 4,
    pad_ending: bool = False,
    paper_size: tuple[float, float] = ...,
): ...

class IncorrectNumberOfPages(Exception): ...
