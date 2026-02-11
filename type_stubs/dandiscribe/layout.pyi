import types
from dandiscribe.data import Margins as Margins
from dandiscribe.enums import PAGESIDE as PAGESIDE
from dandiscribe.exceptions import InvalidSheet as InvalidSheet, NewDocError as NewDocError
from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import Size
from dataclasses import dataclass, field
from functools import lru_cache
from typing import ClassVar, NamedTuple, TypeVar

PAPER_LETTER: Size
PAPER_A4: Size
PAPER_A5: Size

class Page(MixableNamedTuple):
    page_number: int
    size: Size
    master_page: str | None
    is_master: bool
    def as_page(self) -> Page: ...
    def as_master_page(self) -> Page: ...
    def get_margins_and_usable_size(self) -> tuple[Margins, Size]: ...
    def __enter__(self) -> None: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
    def make(self) -> None: ...
    def draw(self, master: str | None = None) -> None: ...

class MasterPage(MixableNamedTuple, Page):
    page_number: ClassVar[None]
    is_master: ClassVar[bool]
    @property
    def name(self) -> str: ...

class SpreadPage(MixableNamedTuple, Page):
    inside_margin: int
    outside_margin: int
    side: PAGESIDE

class Sheet(NamedTuple):
    front: Page
    back: Page
    @property
    @lru_cache
    def size(self) -> Size: ...
Doc = TypeVar('Doc', bound='Document')

@dataclass
class Document:
    pages: list[Page] = field(default_factory=list)
    masterpages: dict[str, MasterPage] = field(default_factory=dict)
    @classmethod
    def create(cls, page_count: int, page_size: Size, create_masters: bool = True, masters_begin: int = 0) -> Doc: ...
    def make(self) -> None: ...
    def draw(self, *draw_args, **draw_kwargs) -> None: ...
