from collections.abc import Sequence
from enum import auto, Enum, IntEnum
from functools import lru_cache, partial
import logging
from logging import handlers
from os import getenv
from pathlib import Path
from typing import Annotated, Callable, NamedTuple, Self
from warnings import warn

from dandiscribe.enums import PAGESIDE
from dandiscribe.util import copy_items, CopyDest, CopySrc
from dandy_lib.annotations import DivisibleBy
from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import Coord, Rect, Size
import scribus

from dandiscribe.data import Margins
from dandiscribe.exceptions import NewDocError, NoObjects
from dandiscribe.layout import Document, Page, PAPER_LETTER

LOG_DIR = Path(
    getenv("LOG_DIR", Path.home().joinpath(".local", "var", "log", "python"))
)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)
LOG_FILE = Path(
    getenv("LOG_FILE", LOG_DIR.joinpath(__name__).with_suffix(".log"))
)

LOGGER = logging.getLogger(__name__)

print(f"log dir `{LOG_DIR}`")

print(f"log path `{LOG_FILE}`")
import sys

# ToRemove
LOGGER.setLevel(logging.DEBUG)

LOGGER.addHandler(logging.StreamHandler())
LOGGER.addHandler(handlers.RotatingFileHandler(LOG_FILE))


def default_suffixer(filename: str | Path) -> Path:
    fpath: Path = Path(filename)
    return fpath.with_stem(f"{fpath.stem}-print")


class LayoutVal(int):
    def __new__(
        cls,
        val: int,
        rows: int,
        cols: int,
        orientation: int = scribus.LANDSCAPE,
    ):
        res = super().__new__(cls, val)
        res.val = val
        res.rows = rows
        res.cols = cols
        res.orientation = orientation
        return res


class Layout(Enum):
    EIGHT_PAGE_MINI = LayoutVal(8, 2, 4)
    QUARTER = LayoutVal(4, 2, 2)
    HALF = LayoutVal(2, 1, 2)

    def __mul__(self: Self, other) -> int:
        return self.value.val * other

    def __add__(self: Self, other) -> int:
        return self.value.val + other

    def __floordiv__(self: Self, other) -> int:
        return self.value.val // other

    def __rfloordiv__(self: Self, other) -> int:
        return self.value.val // other

    @property
    def cols(self) -> int:
        return self.value.cols

    @property
    def rows(self) -> int:
        return self.value.rows

    @property
    def val(self) -> int:
        return self.value.val

    @property
    def orientation(self) -> int:
        return self.value.orientation


class PrintPage(MixableNamedTuple, Page):
    layout: Layout
    is_master = False
    master_page = None
    source_pages: tuple["FinalSheetSpread", ...]

    """
    # Should be covered by new inheritance
    @property
    @lru_cache
    def page_number(self) -> int:
        return self.page.page_number

    # Expose Page methods

    def make(self) -> None:
        return self.page.make()

    def draw(self, master: str | None = None) -> None:
        return self.page.draw(master)

    def get_margins_and_usable_size(self) -> tuple[Margins, Size]:
        return self.page.get_margins_and_usable_size()"""


class SourcePage(Page):
    pass


class FinalSheetSpread(NamedTuple):
    left: int
    right: int

    def translate(
        self,
        source: str,
        dest_page: PrintPage,
        rect: Rect,
        dest_doc: str | None = None,
        scale: float | None = None,
        source_rect: Rect | None = None,
        debug_rects: bool = True,
    ) -> tuple[str | None, str | None]:
        if source_rect is not None:
            scribus.openDoc(source)
            source_size: tuple[float, float] = scribus.getPageNSize(self.left)
            source_rect = Rect(Coord(0, 0), Size.factory(*source_size))
        left_rect = Rect(rect.position, Size(rect.width / 2, rect.height))
        right_rect: Rect = Rect(
            Coord(rect.position.x + rect.width / 2, rect.position.y),
            left_rect.size,
        )
        try:
            left_group = copy_items(
                CopySrc(source, self.left),
                CopyDest(
                    dest_doc if dest_doc is not None else source,
                    dest_page.page_number,
                ),
                debug_boxes=debug_rects,
            )
        except NoObjects:
            left_group = None
        try:
            right_group = copy_items(
                CopySrc(source, self.right),
                CopyDest(
                    dest_doc if dest_doc is not None else source,
                    dest_page.page_number,
                ),
            )
        except NoObjects:
            right_group = None
        return (left_group, right_group)

    def _translate_page(
        self,
        source_page: int,
        dest_page: PrintPage,
        dest_rect: Rect,
        scale: float | None = None,
    ) -> str:

        if scale is None:
            scale: float = 1 / dest_page.layout

        master_page = scribus.getMasterPage(source_page)
        scribus.editMasterPage(master_page)
        scribus.copyObjects(scribus.getAllObjects())
        scribus.closeMasterPage()
        scribus.gotoPage(dest_page.page_number)
        pasted_master: list[str] = scribus.pasteObjects()
        try:
            source_objects = scribus.getAllObjects(page=source_page)
        except ValueError as exc:
            raise ValueError(
                f"Page {source_page} could not be found in {scribus.getDocName()}"
            ) from exc
        if not source_objects:
            raise NoObjects(scribus.getDocName(), scribus.currentPageNumber())
        _send_objects_to_layer(
            "source", send_objects=source_objects, create=True
        )
        scribus.copyObjects(source_objects)
        pasted: list[str] = scribus.pasteObjects()
        _send_objects_to_layer("print", pasted, create=True)
        to_group: list[str] = pasted_master + pasted
        if to_group:
            anchor: str = scribus.createPolyLine(
                [0, scribus.inch * 0.25, 0, 0, 0, scribus.inch * 0.25], "anchor"
            )
            to_group.append(anchor)
        else:
            raise ValueError(f"not enough to group, only found {to_group}")
            return None
        group: str = scribus.setItemName(
            f"page {source_page}", scribus.groupObjects(to_group)
        )
        scribus.scaleGroup(scale, group)
        scribus.moveObjectAbs(dest_rect.x, dest_rect.y, group)

        return group


class FinalSheet(NamedTuple):
    outside: FinalSheetSpread
    inside: FinalSheetSpread


class FinalPageSource(Enum):
    FRONT_START = auto()
    FRONT_END = auto()
    BACK_START = auto()
    BACK_END = auto()


class TranslatePosition(NamedTuple):
    page: int
    position: int


def get_signature_pages(
    page_count: int, signature_sheets: int = 1
) -> list[tuple[int, ...]]:
    LOGGER.info(f"page count // 4 : {page_count // 4}")
    if page_count % 4:
        raise ValueError("Signature pages must be a multiple of 4")
    return [
        tuple[int, ...](
            range((i * signature_sheets) + 1, ((i + 1) * signature_sheets) + 1)
        )
        for i in range(page_count // signature_sheets)
    ]


def front_back_from_signature(signature: Sequence[int]) -> list[FinalSheet]:
    res: list[FinalSheet] = []

    sig_pages = list(signature)

    while sig_pages:
        a, b = sig_pages.pop(0), sig_pages.pop(0)
        z, y = sig_pages.pop(-1), sig_pages.pop(-1)
        res.append(FinalSheet(FinalSheetSpread(z, a), FinalSheetSpread(b, c)))

    return res


class FinalDoc(NamedTuple):
    name: str
    pages: int
    layout: Layout
    signature_sheets: int = 1
    print_page_size: Size = Size(*scribus.PAPER_LETTER)
    margins: Margins = Margins(top=0.5, right=0.5, bottom=0.5, left=0.75)

    @property
    @lru_cache
    def page_usable_size(self) -> Size:
        return Size(
            self.print_page_size.width - self.margins.horizontal,
            self.print_page_size.height - self.margins.vertical,
        )

    @property
    @lru_cache
    def signatures(self) -> int:
        return len(self.signature_pages)

    @property
    @lru_cache
    def cols(self) -> int:
        return self.layout.cols

    @property
    @lru_cache
    def spread_cols(self) -> int:
        return self.layout.cols // 2

    @property
    @lru_cache
    def rows(self) -> int:
        return self.layout.rows

    def export_pdf(
        self: Self,
        options: scribus.PDFfile | None = None,
        path: str | Path | None = None,
    ) -> bool:
        if options is None:
            options = scribus.PDFfile()
        if path is not None:
            options.file = str(path)

        # ToDo: find exceptions where this would fail and return false in that
        #       case
        options.save()
        return True

    @property
    @lru_cache
    def signature_pages(self) -> list[tuple[int, ...]]:
        return get_signature_pages(self.pages, self.signature_sheets)

    @property
    @lru_cache
    def print_pages(self) -> list[PrintPage]:
        source_pages = self.layout * self.pages
        front_pages: list[int] = list(range(1, source_pages + 1))  #  + [-1]
        split_idx = source_pages // 2
        front_pages, back_pages = (
            front_pages[:split_idx],
            front_pages[split_idx:],
        )
        print_pages: list[PrintPage] = []
        LOGGER.debug(
            "source_pages: %i\nfront_pages: %s\nback_pages: %s",
            source_pages,
            front_pages,
            back_pages,
        )
        while front_pages:
            LOGGER.debug(
                "while front pages...\n\tfront: %s\n\tback: %s\n\trows and columns: %i, %i\n\tspread_cols: %i",
                front_pages,
                back_pages,
                self.rows,
                self.cols,
                self.spread_cols,
            )
            front_spreads: list[FinalSheetSpread] = []
            back_spreads: list[FinalSheetSpread] = []
            for row in range(self.rows):
                LOGGER.info("doing row %i", row)
                if not front_pages:
                    assert not back_pages
                    LOGGER.info("breaking in rows")
                    break
                if not self.cols:
                    raise ValueError("no cols")
                for col in range(self.spread_cols):
                    LOGGER.info(
                        f"r,c: {row},{col}\nf, b: {front_pages}, {back_pages}"
                    )
                    if not front_pages:
                        assert not back_pages
                        warn("breaking in cols")
                        break
                    front_spreads.append(
                        FinalSheetSpread(front_pages.pop(-1), back_pages.pop(0))
                    )
                    back_spreads.append(
                        FinalSheetSpread(back_pages.pop(0), front_pages.pop(-1))
                    )
                else:
                    continue
                break

            if not isinstance(self.print_page_size, Size):
                raise ValueError(f"Wrong Size(): {self.print_page_size}")
            print_pages.extend(
                [
                    PrintPage(
                        len(print_pages) + 1,
                        self.layout,
                        tuple[FinalSheetSpread, ...](front_spreads),
                        self.print_page_size,
                    ),
                    PrintPage(
                        len(print_pages) + 2,
                        self.layout,
                        tuple[FinalSheetSpread, ...](back_spreads),
                        self.print_page_size,
                    ),
                ]
            )
        pg_range: int = self.pages // self.layout + (
            1 if self.pages % self.layout.val else 0
        )
        for print_pg in range(pg_range):
            LOGGER.debug("for pg (%i) in print_pgs (%i)", print_pg, pg_range)

        return print_pages

    def assemble(
        self,
        source: str | Path | None = None,
        close_source: bool = True,
        close_final: bool = True,
    ):

        if source is None:
            scribus.saveDoc()
            source = scribus.getDocName()
        else:
            scribus.openDoc(str(source))

        source_pages: int = scribus.pageCount()

        # Ensure new_name is a path object
        new_name = Path(self.name)
        assert new_name != Path(scribus.getDocName())
        """
        try:
            scribus.setPageSize(self.print_page_size)
        except AttributeError as exc:
            # pre 1.7 scribus
            raise EnvironmentError(f"pre 1.7 scribus, could not resize page in script (scribus version is {scribus.SCRIBUS_VERSION_INFO})") from exc
        """

        # ToDo ensure uniform page size
        source_size: tuple[float, float] = scribus.getPageNSize(1)
        source_unit: int = scribus.getUnit()

        size_in_units = tuple(
            scribus.pointsToDocUnit(val) for val in self.print_page_size
        )

        LOGGER.warning(get_signature_pages(source_pages, self.signature_sheets))
        if not scribus.newDocument(
            size_in_units,
            self.margins,
            self.layout.orientation,
            1,
            source_unit,
            scribus.PAGE_1,
            1,
            self.pages,
        ):
            raise NewDocError()
        scribus.setDocType(scribus.NOFACINGPAGES, scribus.FIRSTPAGELEFT)
        scribus.saveDocAs(str(new_name))
        # upda
        print(f"page count: {scribus.pageCount()}")
        page_dims: dict[int, tuple[float, float]] = dict[
            int, tuple[float, float]
        ](
            (page_no, scribus.getPageNSize(page_no))
            for page_no in range(1, scribus.pageCount() + 1)
        )

        for print_page in self.print_pages:

            scribus.gotoPage(print_page.page_number)

            scribus.setCurrentPageSize(
                *[dim * scribus.inch for dim in self.print_page_size]
            )
            col = 0
            row = 0

            x: float = self.margins.left
            y: float = self.margins.top

            col_width: float = float(self.page_usable_size.width / self.cols)
            row_height: float = float(self.page_usable_size.height / self.rows)
            spread_page_width: float = col_width / 2.0

            for spread in print_page.source_pages:
                _ = spread.translate(
                    str(source),
                    print_page,
                    Rect(Coord(x, y), Size(col_width, row_height)),
                    self.name,
                    debug_rects=True,
                )
                # Setup for next spread
                if col == self.spread_cols - 1:
                    row += 1
                    col = 0
                    x = self.margins.left
                    y += row_height
                else:
                    col += 1
                    x += col_width

        if close_final:
            assert scribus.getDocName() == self.name
            scribus.closeDoc()

        elif close_source:
            assert scribus.haveDoc() >= 2
            scribus.openDoc(str(source))
            scribus.closeDoc()
            assert scribus.getDocName() == self.name


HALF_DOC: partial[FinalDoc] = partial[FinalDoc](FinalDoc, layout=Layout.HALF)
QUARTER_DOC: partial[FinalDoc] = partial[FinalDoc](
    FinalDoc, layout=Layout.QUARTER
)


def _send_objects_to_layer(
    layer_name: str, send_objects: list[str], create: bool = False
):
    for send_object in send_objects:
        _ = _send_to_layer(layer_name, send_object, create=create)


def _send_to_layer(
    layer_name: str, send_object: str | None = None, create: bool = False
) -> bool:
    if send_object is not None:
        do_send = partial(scribus.sendToLayer, name=send_object)

    else:
        do_send: Callable[[str], None] = scribus.sendToLayer
    try:
        do_send(layer_name)
    except (scribus.NotFoundError, scribus.ScribusException) as exc:
        if create:
            # Layer not found, create it
            scribus.createLayer(layer_name)
            return _send_to_layer(
                layer_name, send_object=send_object, create=False
            )
        else:
            raise exc
    else:
        return True


def generate_pages(
    total_pages: int,
    signature_size: Annotated[int, DivisibleBy(4)] = 4,
    pad: bool = False,
    has_cover: bool = True,
    has_title_page: bool = False,
    has_toc: bool = True,
    start_side: PAGESIDE = PAGESIDE.RIGHT,
    offset_start: int = 0,
    print_size: Size = PAPER_LETTER,
    layout: Layout = Layout.QUARTER,
) -> None:
    """
    just brute force it for now
    """
    if total_pages % signature_size and not pad:
        raise ValueError("incorrect number of pages for signature size")
    page_dims = Size(
        print_size.width / layout.portrait_cols,
        print_size.height / layout.portrait_rows,
    )
    doc: Document = Document.create(total_pages, page_dims)

    print(doc)
    doc.make()
    doc.draw()


def get_page_and_pos(
    source_page: int, total_pages: int, Layout: Layout, signature_size: int = 1
) -> TranslatePosition:
    pages = list(range(total_pages))
    if source_page < total_pages / 2:
        # first half of book, move front from center
        pass
    else:
        # second half, move back from center
        pass
    first_half = pages[: int(total_pages / 2)]
    second_half = pages[int(total_pages) / 2 :]


def create_from_current_doc(
    layout: Layout,
    signature_sheets=4,
    pad_ending=False,
    paper_size: tuple[float, float] = scribus.PAPER_LETTER,
):  # scribus.PAPER_LETTER):

    page_count: int = scribus.pageCount() // layout
    remainder_pages: int = scribus.pageCount() % layout
    if not pad_ending and remainder_pages:
        raise IncorrectNumberOfPages()
    elif remainder_pages:
        page_count += 1

    print_doc = FinalDoc(
        scribus.getDocName(),
        layout=layout,
        signature_sheets=signature_sheets,
        pages=page_count,
        print_page_size=Size.factory(*paper_size),
    )

    print_doc.assemble(source=None)


class IncorrectNumberOfPages(Exception):
    pass
