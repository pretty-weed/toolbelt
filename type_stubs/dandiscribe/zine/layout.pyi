import scribus
from _typeshed import Incomplete
from collections.abc import Sequence
from dandiscribe.data import Margins as Margins, Rect as Rect, Size as Size
from dandiscribe.enums import (
    InsertPaddingPages as InsertPaddingPages,
    Orientation as Orientation,
    PAGESIDE as PAGESIDE,
    PaperSize as PaperSize,
    Unit as Unit,
)
from dandiscribe.exceptions import (
    NewDocError as NewDocError,
    NoObjects as NoObjects,
    PageOutOfRange as PageOutOfRange,
    ScriptRunError as ScriptRunError,
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
from enum import Enum
from functools import lru_cache, partial
from multiprocessing import Value as Value
from pathlib import Path
from re import S as S
from typing import Annotated, NamedTuple
from warnings import warn as warn

LOG_DIR: Incomplete
LOG_FILE: Incomplete
LOGGER: Incomplete

def default_suffixer(filename: str | Path) -> Path: ...

class LayoutVal:
    val: int
    rows: int
    cols: int
    orientation: Orientation
    page_rotations: Incomplete
    def __init__(
        self,
        val: int,
        rows: int,
        cols: int,
        orientation: Orientation = ...,
        page_rotations: dict[int, int | float] | None = None,
    ) -> None: ...
    def __int__(self) -> int: ...
    def get_enum_tuple(self) -> tuple[int, int, int, int]: ...

class Layout(ChoiceEnumMixin, LayoutVal, Enum, metaclass=ChoiceEnumMeta):
    EIGHT_PAGE_MINI = ...
    QUARTER = ...
    QUARTER_PORTRAIT = ...
    QUARTER_LANDSCAPE = ...
    HALF = (2, 1, 2)
    def __mul__(self, other: float | int) -> int | float: ...
    def __add__(self, other: float | int) -> int | float: ...
    def __floordiv__(self, other: float | int) -> int | float: ...
    def __rfloordiv__(self, other: float | int) -> int | float: ...
    def __rtruediv__(self, other: int | float) -> int | float: ...

class PrintPage(MixableNamedTuple, Page):
    layout: Layout
    is_master: bool
    master_page: Incomplete
    spreads: tuple["FinalSheetSpread", ...]
    rotations: tuple[tuple[int, int | float]] | None
    def max(self) -> int | float: ...
    def get_source_pages(self) -> list[int]: ...

class SourcePage(Page): ...

class FinalSheetSpread(NamedTuple):
    left: int | None
    right: int | None
    left_rotation: int | float | None = ...
    right_rotation: int | float | None = ...
    def max(self) -> int | float: ...
    def __bool__(self) -> bool: ...
    def sorted(
        self, reverse: bool = False, skip_missing: bool = False
    ) -> list[int | float]: ...
    def translate(
        self,
        source: str,
        dest_page: PrintPage,
        rect: Rect,
        dest_doc: str | None = None,
        source_rect: Rect | None = None,
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
    def signature_pages(self) -> list[tuple[int, ...]]: ...
    def get_print_pages(
        self,
        insert_padding_pages: InsertPaddingPages = ...,
        insert_doc_pages: bool = False,
        source_pg_count: int | None = None,
    ) -> list[PrintPage]: ...
    def assemble(
        self,
        source: str | Path | None = None,
        close_source: bool = True,
        close_final: bool = True,
        inside_margins: bool = False,
        insert_padding_pages: InsertPaddingPages = ...,
        insert_doc_pages: bool = False,
    ) -> None: ...

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
