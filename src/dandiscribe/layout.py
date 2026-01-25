from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Literal, NamedTuple

from dandiscribe.enums import PAGESIDE
from dandiscribe.exceptions import InvalidSheet
import scribus

from dandy_lib.datatypes.twodee import Size

from dandiscribe.data import Margins


class Page(NamedTuple):
    page_number: int
    size: Size = Size.factory(*scribus.PAPER_A5)
    master_page: str | None = None
    is_master: bool = False

    def __post_init__(self):
        try:
            if self.size.height <= 0:
                raise ValueError("height must be greater than zero")
            elif self.size.width <= 0:
                raise ValueError("width must be greater than zero")
        except AttributeError:
            raise TypeError("Page size must be a Size() object")

    def as_page(self) -> "Page":
        return self.__class__(**(self.__dict__ | {"is_master": False}))

    def as_master_page(self) -> "Page":
        return self.__class__(**(self.__dict__ | {"is_master": True}))

    def _get_margins_and_usable_size(self) -> tuple[Margins, Size]:
        try:
            margins = Margins(*scribus.getPageMargins())
        except TypeError as exc:
            raise TypeError(f"value is {scribus.getPageMargins()}") from exc
        return (
            margins,
            Size(
                self.size.width - margins.right - margins.left,
                self.size.height - margins.top - margins.bottom,
            ),
        )

    def __enter__(self):
        if self.is_master:
            assert self.master_page
            if self.master_page not in scribus.masterPageNames():
                self.make()
            scribus.editMasterPage(self.master_page)
        else:
            assert self.page_number
            if self.page_number >= scribus.pageCount():
                self.make()

            scribus.gotoPage(self.page_number)

    def __exit__(self, type, value, traceback):
        if self.is_master:
            scribus.closeMasterPage()

    def make(self):
        if self.is_master:
            scribus.createMasterPage(self.master_page)
            return

        while self.page_number >= scribus.pageCount():
            scribus.newPage(-1, self.master_page)

    def draw(self, master: str | None = None):
        if self.is_master:
            return
        draw_master: str | Literal[True] = master is None or master

        if not any([self.is_master, draw_master, self.master_page is None]):
            scribus.applyMasterPage(self.master_page, self.page_number)


@dataclass(kw_only=True)
class SpreadPage(Page):
    inside_margin: int
    outside_margin: int
    side: PAGESIDE


class Sheet(NamedTuple):
    front: Page
    back: Page

    @lru_cache
    @property
    def size(self) -> Size:
        fs: Size = self.front.size
        bs: Size = self.back.size
        if not any([fs >= bs, fs <= bs]):
            msg: str = (
                "If sheet front and back are of different sizes, one must be larger in both dimensions"
            )
            raise InvalidSheet(msg)
        elif bs > fs:
            return bs
        return fs
