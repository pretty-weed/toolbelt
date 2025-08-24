from dataclasses import field, MISSING
import datetime
from functools import cache

import scribus

from dandiscribe.data import frozen_dataclass, Margins, Size
from dandiscribe.enums import PAGESIDE


@frozen_dataclass
class Page:
    page_number: int = None
    size: Size = field(default=Size(*scribus.PAPER_A5))
    master_page: str = None
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

    @cache
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

    def get_delta_date(self, days=0, weeks=0) -> tuple[datetime.date, bool]:
        dd = self.page_date + datetime.timedelta(days=days, weeks=week)
        return dd, dd.month == self.page_date.month

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

    def draw(self, master=None):
        if self.is_master:
            return
        draw_master = master is None or master

        if not any([self.is_master, draw_master, self.master_page is None]):
            scribus.applyMasterPage(self.master_page, self.page_number)


@frozen_dataclass
class SpreadPage(Page):
    side: PAGESIDE

    def __post_init__(self):
        if self.side is None or self.side is MISSING:
            raise TypeError("side must be provided as keyword")
