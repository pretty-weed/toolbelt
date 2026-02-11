from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, ClassVar, Literal, NamedTuple, Self, TypeVar

from dandiscribe.enums import PAGESIDE
from dandiscribe.exceptions import InvalidSheet, NewDocError
import scribus

from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import Size

from dandiscribe.data import Margins


PAPER_LETTER: Size = Size(*scribus.PAPER_LETTER)
PAPER_A4: Size = Size(*scribus.PAPER_A4)
PAPER_A5: Size = Size(*scribus.PAPER_A5)
class Page(MixableNamedTuple):
    page_number: int
    size: Size = Size.factory(*scribus.PAPER_A5)
    master_page: str | None = None
    is_master: bool = False

    def as_page(self) -> "Page":
        return self.__class__(**(self.__dict__ | {"is_master": False}))

    def as_master_page(self) -> "Page":
        return self.__class__(**(self.__dict__ | {"is_master": True}))

    def get_margins_and_usable_size(self) -> tuple[Margins, Size]:
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

    def draw(self, master: str | None = None) -> None:
        if self.is_master:
            return
        draw_master: str | Literal[True] = master is None or master

        if not any([self.is_master, draw_master, self.master_page is None]):
            scribus.applyMasterPage(self.master_page, self.page_number)


class MasterPage(MixableNamedTuple, Page):
    """
    ToDo: when I can mask out things from namespace by making them class attrs
    """
    page_number: ClassVar[None] = None
    is_master: ClassVar[bool] = True

    @property
    def name(self) -> str:
        return self.master_page

class SpreadPage(MixableNamedTuple, Page):
    inside_margin: int
    outside_margin: int
    side: PAGESIDE


class Sheet(NamedTuple):
    front: Page
    back: Page

    
    @property
    @lru_cache
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


# Create a generic variable that can be 'Parent', or any subclass.
Doc = TypeVar('Doc', bound='Document')

@dataclass
class Document:
    pages: list[Page] = field(default_factory=list)
    masterpages: dict[str, MasterPage] = field(default_factory=dict)

    @classmethod
    def create(cls: type[Doc], page_count: int, page_size: Size, create_masters: bool = True, masters_begin: int = 2) -> Doc:
        if create_masters:
            masters = dict((mpname, MasterPage(page_size, mpname)) for mpname in [f"{side}-default" for side in ["left", "right"]])
        else:
            masters = {}
        master_pages: tuple[str, str] = ("left-default", "right-default")
        doc = cls(
            [
                Page(
                    pg_num, page_size, 
                    master_page=
                        (
                            master_pages[pg_num % len(masters)] 
                            if masters and masters_begin <= pg_num else None
                        ) 
                ) 
                for pg_num in range(1, page_count + 1)
            ], 
            masters,
        )

        return cls
    def make(self):
        assert len(set(page.size for page in self.pages)) == 1
        if not scribus.newDocument(
            tuple(self.pages[0].size),
            (10, 10, 10, 15),
            scribus.PORTRAIT,
            1,
            scribus.UNIT_POINTS,
            scribus.PAGE_2,
            1,
            len(self.pages),
        ):
            raise NewDocError()

        # Setup the master pages


    def draw(self, *draw_args, **draw_kwargs):
        # make master pages
        scribus.progressReset()
        mp_count = len(set(page.master_page for page in self.pages))
        total = mp_count + len(self.pages)
        done = 0
        master_kwargs = draw_kwargs.get("master_kwargs", draw_kwargs)
        for page in self.pages:
            if page.master_page is not None and page.master_page not in self.masterpages:
                scribus.progressSet((done + 1) // total)
                master_page = page.as_master_page()
                self.masterpages[page.master_page] = master_page
                master_page.draw(master=True, *draw_kwargs, **master_kwargs)
                done += 1

                assert all([pg.is_master for pg in self.masterpages.values()])
                assert not any([pg.is_master for pg in self.pages])

        # make pages
        for page in self.pages:
            scribus.progressSet((done + 1) // total)
            page.draw(
                master=False, *draw_args, **draw_kwargs
            )
            done += 1

