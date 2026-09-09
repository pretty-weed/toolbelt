from collections.abc import Sequence
from copy import copy
from enum import auto, Enum
from functools import lru_cache, partial
import logging
from logging import handlers
from multiprocessing import Value
from os import getenv
from pathlib import Path
from re import S
import sys
from typing import Annotated, Callable, Literal, NamedTuple, Self
from warnings import warn


from dandy_lib.annotations import DivisibleBy
from dandy_lib.cli.enums import ChoiceEnumMixin, ChoiceEnumMeta
from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import Coord


from dandiscribe.data import Margins, Rect, Size
from dandiscribe.enums import (
    PAGESIDE,
    InsertPaddingPages,
    Orientation,
    PaperSize,
    Unit,
)
from dandiscribe.exceptions import (
    NewDocError,
    NoObjects,
    PageOutOfRange,
    ScriptRunError,
)
from dandiscribe.layout import Document, Page, PAPER_LETTER
from dandiscribe.util import copy_items, CopyDest, CopySrc
import scribus


LOG_DIR = Path(
    getenv("LOG_DIR", Path.home().joinpath(".local", "var", "log", "python"))
)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)
LOG_FILE = Path(
    getenv("LOG_FILE", LOG_DIR.joinpath(__name__).with_suffix(".log"))
)

LOGGER = logging.getLogger(__name__)


# ToRemove
LOGGER.setLevel(logging.DEBUG)

LOGGER.addHandler(logging.StreamHandler())
LOGGER.addHandler(handlers.RotatingFileHandler(LOG_FILE))


def default_suffixer(filename: str | Path) -> Path:
    fpath: Path = Path(filename)
    return fpath.with_stem(f"{fpath.stem}-print")


class LayoutVal:
    def __init__(
        self,
        val: int,
        rows: int,
        cols: int,
        orientation: Orientation = Orientation.LANDSCAPE,
        page_rotations: dict[int, int | float] | None = None,
    ) -> None:
        self.val: int = val
        self.rows: int = rows
        self.cols: int = cols
        self.orientation: Orientation = orientation
        self.page_rotations = page_rotations
        super().__init__()

    def __int__(self) -> int:
        return self.val

    def get_enum_tuple(self) -> tuple[int, int, int, int]:
        return (self.val, self.rows, self.cols, self.orientation)


class Layout(ChoiceEnumMixin, LayoutVal, Enum, metaclass=ChoiceEnumMeta):
    EIGHT_PAGE_MINI = (
        8,
        2,
        4,
        Orientation.LANDSCAPE,
        dict[int, int | float]([(1, 180), (6, 180), (7, 180), (8, 180)]),
    )
    QUARTER = (4, 2, 2, Orientation.PORTRAIT)

    QUARTER_PORTRAIT = (4, 2, 2, Orientation.PORTRAIT)
    QUARTER_LANDSCAPE = (4, 2, 2, Orientation.LANDSCAPE)
    HALF = (2, 1, 2)

    def __mul__(self: Self, other: float | int) -> int | float:
        return self.val * other

    def __add__(self: Self, other: float | int) -> int | float:
        return self.val + other

    def __floordiv__(self: Self, other: float | int) -> int | float:
        return self.val // other

    def __rfloordiv__(self: Self, other: float | int) -> int | float:
        return self.val // other

    def __rtruediv__(self: Self, other: int | float) -> int | float:
        return other / self.val


class PrintPage(MixableNamedTuple, Page):
    layout: Layout
    is_master = False
    master_page = None
    spreads: tuple["FinalSheetSpread", ...]
    rotations: tuple[tuple[int, int | float]] | None = None

    def max(self) -> int | float:
        return max(spread.max() for spread in self.spreads)

    def get_source_pages(self) -> list[int]:
        return list(
            sorted(sum((list(spread) for spread in self.spreads if spread), []))
        )


class SourcePage(Page):
    pass


class FinalSheetSpread(NamedTuple):
    left: int | None
    right: int | None
    left_rotation: int | float | None = None
    right_rotation: int | float | None = None

    def max(self) -> int | float:

        try:
            return max(v for v in self if v is not None)
        except ValueError:
            return float("-inf")

    def __bool__(self) -> bool:
        return any(p is not None for p in self)

    def sorted(
        self, reverse: bool = False, skip_missing: bool = False
    ) -> list[int | float]:
        if skip_missing:
            return sorted([v for v in self if v is not None])
        return sorted(
            [v if v is not None else float("-inf") for v in self],
            reverse=reverse,
        )

    def translate(
        self,
        source: str,
        dest_page: PrintPage,
        rect: Rect,
        dest_doc: str | None = None,
        source_rect: Rect | None = None,
    ) -> tuple[str | None, str | None]:

        for source_page in self.sorted(skip_missing=True):
            if source_rect is not None:
                break
            scribus.openDoc(source)
            try:
                source_size: tuple[float, float] = tuple[float, float](
                    scribus.docUnitToPoints(d)
                    for d in scribus.getPageNSize(source_page)
                )
            except IndexError as exc:
                raise PageOutOfRange(source_page, source)
            source_rect = Rect(
                Coord(0, 0), Size.factory(*source_size, unit=Unit.POINTS)
            )

            LOGGER.debug(
                "no source rect passed to FinalSheetSpread.translate(), so generated one:\n\t%s",
                source_rect,
            )
        left_rect: Rect = Rect(
            rect.position,
            Size(rect.width / 2, rect.height, rect.unit).as_points(),
        )
        right_rect: Rect = Rect(
            Coord(rect.position.x + rect.width / 2, rect.position.y),
            Size(rect.width / 2, rect.height, rect.unit).as_points(),
        )
        LOGGER.debug("left rect: %s", left_rect)
        LOGGER.debug("right rect: %s", right_rect)
        completed: dict[int, str] = dict[int, str]()
        dest_doc = dest_doc if dest_doc is not None else source
        for source_page in self.sorted(skip_missing=True):
            src = CopySrc(source, source_page)
            dest = CopyDest(dest_doc, dest_page.page_number)
            dest_box = left_rect if source_page == self.left else right_rect

            rotation = (
                self.left_rotation
                if source_page == self.left
                else self.right_rotation
            )
            try:
                this_group = copy_items(
                    src,
                    dest,
                    source_box=source_rect,
                    target_box=dest_box,
                    rotation=rotation,
                )
            except NoObjects:
                # Skip this page, the other might work if this is the first
                continue
            except PageOutOfRange:
                # we sorted pages, so if we hit this, no sense continuing
                break
            else:
                completed[source_page] = this_group

        return (completed.get(self.left), completed.get(self.right))

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
    signature_sheets: int = 2
    print_page_size: Size = Size(*scribus.PAPER_LETTER)
    unit: Unit = Unit.POINTS

    margins: Margins = Margins(top=0.5, right=0.5, bottom=0.5, left=0.75)

    @property
    @lru_cache
    def page_size(self) -> Size:
        if self.layout.orientation == scribus.PORTRAIT:
            return Size(
                min(self.print_page_size),
                max(self.print_page_size),
                unit=self.unit,
            )
        return Size(
            max(self.print_page_size), min(self.print_page_size), unit=self.unit
        )

    @property
    @lru_cache
    def page_usable_size(self) -> Size:
        if self.unit == self.print_page_size.unit:
            return Size(
                self.page_size.width - self.margins.horizontal,
                self.page_size.height - self.margins.vertical,
                self.unit,
            )
        conv_factor = print_page_size.unit @ self.unit
        return Size(
            self.page_size.width * conv_factor - self.margins.horizontal,
            self.page_size.height * conv_factor - self.margins.vertical,
            self.unit,
        )

    @property
    @lru_cache
    def page_usable_size_pt(self) -> Size:
        ratio: float = self.unit @ Unit.POINTS
        return Size(
            ratio * (self.page_size.width - self.margins.horizontal),
            ratio * (self.page_size.height - self.margins.vertical),
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
    def signature_pages(self) -> list[tuple[int, ...]]:
        return get_signature_pages(self.pages, self.signature_sheets)

    def get_print_pages(
        self,
        insert_padding_pages: InsertPaddingPages = InsertPaddingPages.NO,
        insert_doc_pages: bool = False,
        source_pg_count: int | None = None,
    ) -> list[PrintPage]:
        source_pages: list[int | None] = list(
            range(1, int(self.layout) * self.pages + 1)
        )
        LOGGER.debug(
            f"initial source pages for pg count %s: %s",
            source_pg_count,
            source_pages,
        )
        if source_pg_count is not None and source_pg_count != len(source_pages):

            discrepancy: int = len(source_pages) - source_pg_count
            if discrepancy % self.signature_pages:
                pass
            # adjust pages for padding and/or adding doc pages
            LOGGER.warning(
                f"adjusting page count %d -> %d",
                source_pg_count,
                len(source_pages),
            )
            if source_pg_count > len(source_pages) and not insert_doc_pages:
                LOGGER.debug("too many source pages for doc")
                raise ValueError("Too many source pages for document")
            elif source_pg_count > len(source_pages):
                # throw this pass in here, since with this we can assume that
                # that source_pg_count < insert_padding_pages
                LOGGER.debug(
                    "source page count is greater than desired source pages"
                )
                pass
            elif insert_padding_pages == InsertPaddingPages.BEGINNING:
                # offset pages
                LOGGER.debug("Inserting %d pages at beginning", discrepancy)
                source_pages[:discrepancy] = [None] * discrepancy
                source_pages[discrepancy:] = [
                    i - discrepancy if i is not None else None
                    for i in source_pages[discrepancy:]
                ]
            elif insert_padding_pages == InsertPaddingPages.END:
                LOGGER.debug("Inserting %d pages at end", discrepancy)
                source_pages[-discrepancy:] = [None] * discrepancy
            else:
                exc = ValueError(
                    "Not padding pages, and source page count doesn't match document"
                )
                # this nonsense is to log the exception immediately then raise
                try:
                    raise exc
                except ValueError as e:
                    LOGGER.exception("Something went wrong getting print pages")
                    raise e

        front_pages: list[int] = copy(source_pages)
        assert not len(front_pages) % 2
        split_idx = len(front_pages) // 2
        front_pages, back_pages = (
            front_pages[:split_idx],
            front_pages[split_idx:],
        )
        print_pages: list[PrintPage] = []
        LOGGER.debug(
            "source_pages: %s\nfront_pages: %s\nback_pages: %s",
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
                        LOGGER.debug(
                            "breaking in cols at row: %d col: %d", row, col
                        )
                        break
                    if self.layout.page_rotations is not None:
                        fl_rot: int | float | None = (
                            self.layout.page_rotations.get(front_pages[-1])
                        )
                        fr_rot: int | float | None = (
                            self.layout.page_rotations.get(back_pages[0])
                        )
                        bl_rot: int | float | None = (
                            self.layout.page_rotations.get(back_pages[1])
                        )
                        br_rot: int | float | None = (
                            self.layout.page_rotations.get(front_pages[-2])
                        )
                    else:
                        fl_rot = fr_rot = bl_rot = br_rot = None

                    front_spreads.append(
                        FinalSheetSpread(
                            front_pages.pop(-1),
                            back_pages.pop(0),
                            left_rotation=fl_rot,
                            right_rotation=fr_rot,
                        )
                    )
                    back_spreads.append(
                        FinalSheetSpread(
                            back_pages.pop(0),
                            front_pages.pop(-1),
                            left_rotation=bl_rot,
                            right_rotation=br_rot,
                        )
                    )
                else:
                    continue
                break

            if not isinstance(self.print_page_size, PaperSize):
                raise ValueError(
                    f"Wrong Size(): {self.print_page_size} ({repr(self.print_page_size)})"
                )
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
        inside_margins: bool = False,
        insert_padding_pages: InsertPaddingPages = InsertPaddingPages.NO,
        insert_doc_pages: bool = False,
    ) -> None:

        current_doc: str
        resize_pages = False
        if source is None:
            scribus.saveDoc()
            source: Path = Path(scribus.getDocName())
            resize_pages = True
        else:
            try:
                scribus.openDoc(str(source))
            except Exception as exc:
                print(exc)
                print(Path(source))
                print(list(Path(source).parent.glob("*")))
                raise exc
        make_pages = self.pages
        source_pages: int = scribus.pageCount()
        if source_pages % int(self.layout) and not insert_padding_pages:
            raise ValueError(
                f"Source document pages ({source_pages}) does not divide evenly into Layout (//{self.layout})"
            )
        if (
            source_pages // int(self.layout) != self.pages
            and not insert_padding_pages
        ):
            raise ValueError(
                f"Final doc format ([source pgs]{source_pages}//[layout pgs]{int(self.layout)}) does not fit number of pages in doc ({self.pages})"
            )
        # Ensure new_name is a path object
        new_name = Path(self.name)
        if new_name == Path(scribus.getDocName()):
            raise ValueError(
                "FinalDoc.assemble() not made to target source document"
            )

        # ToDo ensure uniform page size
        source_size_pt: Size = Size.factory(
            *(scribus.docUnitToPoints(dim) for dim in scribus.getPageNSize(1)),
            unit=Unit.POINTS,
        )
        source_unit = Unit.get_current()
        conv_factor: float = source_unit @ Unit.POINTS

        LOGGER.debug("creating new doc %s with %d pages", self.name, self.pages)

        try:

            success: bool = scribus.newDocument(
                self.print_page_size.for_scribus(),
                self.margins,
                self.layout.orientation,
                1,
                int(self.unit),
                scribus.PAGE_1,
                1,
                self.pages,
            )
            if not success:
                raise NewDocError()
        except Exception as exc:
            LOGGER.exception(f"Exception raised when creating doc: {exc}\n")
            raise exc

        scribus.setDocType(scribus.NOFACINGPAGES, scribus.FIRSTPAGELEFT)
        try:
            scribus.saveDocAs(str(new_name))
        except Exception as exc:
            LOGGER.exception("Failed to save %s", new_name)
            raise exc
        # update
        page_dims: dict[int, tuple[float, float]] = dict[
            int, tuple[float, float]
        ](
            (page_no, scribus.getPageNSize(page_no))
            for page_no in range(1, scribus.pageCount() + 1)
        )
        print_pages: list[PrintPage] = self.get_print_pages(
            insert_padding_pages, insert_doc_pages, source_pages
        )
        max_source: int | float = max(pp.max() for pp in print_pages)
        LOGGER.debug("max_source is %d", max_source)
        for print_page in print_pages:

            try:
                scribus.gotoPage(print_page.page_number)
            except IndexError as exc:
                # ToDo figure out where to put this with front cover/etc
                # just assuming will not put on front cover, so either cover or
                # inside of it, in case there are important things there

                raise PageOutOfRange(print_page.page_number, self.name) from exc

            if resize_pages:
                LOGGER.warning("resizing pages in existing doc")
                scribus.setCurrentPageSize(
                    *[dim * self.unit for dim in self.print_page_size]
                )
            else:
                LOGGER.info("Not resizing pages")
            col = 0
            row = 0

            x_reset = self.margins.left * conv_factor if inside_margins else 0.0

            x: float = x_reset
            y: float = self.margins.top if inside_margins else 0.0

            # the cols are for pages, not spreads
            pts_size = (
                self.page_usable_size_pt
                if inside_margins
                else self.page_size.as_points()
            )
            spread_width: float = float(pts_size.width / (self.cols // 2))
            row_height: float = float(pts_size.height / self.rows)
            for spread in print_page.spreads:

                try:
                    left_grp, right_grp = spread.translate(
                        str(source),
                        print_page,
                        Rect(
                            Coord(x, y),
                            Size(spread_width, row_height, Unit.POINTS),
                        ),
                        self.name,
                    )
                except PageOutOfRange as exc:
                    if not insert_padding_pages:
                        raise exc
                # Setup for next spread
                if col == self.spread_cols - 1:
                    row += 1
                    col = 0
                    x = x_reset
                    y += row_height
                else:
                    col += 1
                    x += spread_width

        scribus.saveDoc()
        if close_final:
            current_doc = scribus.getDocName()

            LOGGER.info("closing final doc: %s", current_doc)
            if current_doc != self.name:
                raise ScriptRunError(
                    f"Expected final doc to be open before closing, got {current_doc}"
                )
            scribus.closeDoc()

        if close_source:
            if not close_final:
                LOGGER.debug("closing source, but not final")
                doc_count: int = scribus.haveDoc()
                if not doc_count >= 2:
                    raise ScriptRunError(
                        f"Expected two docs open (source and final), got {doc_count}",
                        expected=2,
                        actual=doc_count,
                    )
                scribus.openDoc(str(source))
                scribus.saveDoc()

            LOGGER.debug(
                "about to close source doc. Current doc: %s",
                scribus.getDocName(),
            )
            current_doc = scribus.getDocName()
            if not current_doc == str(source):
                raise ScriptRunError(
                    f"Expected to be on source doc ({source}), but {current} is open.",
                    expected=source,
                    actual=current_doc,
                )
            scribus.closeDoc()


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

    doc.make()
    doc.draw()


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
