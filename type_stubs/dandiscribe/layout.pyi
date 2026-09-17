import logging
import types
from dandiscribe.data import Margins as Margins
from dandiscribe.enums import PAGESIDE as PAGESIDE
from dandiscribe.exceptions import (
    InvalidSheet as InvalidSheet,
    NewDocError as NewDocError,
)
from dandiscribe.log import configure as configure
from dandy_lib.datatypes.twodee import Size
from dataclasses import dataclass, field
from functools import lru_cache
from typing import NamedTuple, Self, TypeVar, override

LOGGER: logging.Logger
PAPER_LETTER: Size
PAPER_A4: Size
PAPER_A5: Size

@dataclass
class Page:
    page_number: int = ...
    size: Size = ...
    master_page: str | None = ...
    is_master: bool = ...
    def as_page(self) -> Self: ...
    def get_master_page(self) -> MasterPage: ...
    def get_margins_and_usable_size(self) -> tuple[Margins, Size]: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        type: type[BaseException] | None,
        value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def make(self) -> None: ...
    def draw(self, bake_master: bool = False) -> None: ...

@dataclass
class MasterPage(Page):
    is_master: bool = field(default=True, init=False)
    @property
    def name(self) -> str: ...
    @override
    def draw(self) -> None: ...

@dataclass
class SpreadPageMixin:
    inside_margin: float = ...
    outside_margin: float = ...
    side: PAGESIDE = ...

@dataclass
class SpreadPage(Page, SpreadPageMixin): ...

class Sheet(NamedTuple):
    front: Page
    back: Page
    @property
    @lru_cache
    def size(self) -> Size: ...

Doc = TypeVar("Doc", bound="Document")

def get_mpage_sizes() -> dict[str, Size]: ...
@dataclass
class Document:
    pages: list[Page] = field(default_factory=list)
    masterpages: dict[str, MasterPage] = field(default_factory=dict)
    @classmethod
    def from_current(cls) -> Self: ...
    @classmethod
    def create(
        cls,
        page_count: int,
        page_size: Size,
        create_masters: bool = True,
        masters_begin: int = 2,
    ) -> Self: ...
    def make(self) -> None: ...
    def draw(self, *draw_args, **draw_kwargs) -> None: ...
