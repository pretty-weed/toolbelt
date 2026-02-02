from ast import Call
from bdb import set_trace
import enum
from functools import cache, lru_cache, partial
from math import remainder
from multiprocessing import Value
from pathlib import Path
from typing import Any, Callable, NamedTuple, Self
from warnings import warn

from dandy_lib.datatypes.tuples import MixableNamedTuple
from dandy_lib.datatypes.twodee import Coord, Rect, Size
import scribus

from dandiscribe.data import Margins
from dandiscribe.exceptions import NewDocError
from dandiscribe.layout import Page


def default_suffixer(filename: str | Path) -> Path:
    filename: Path = Path(filename)
    return filename.with_stem(f"{filename.stem}-print")


class Layout(enum.IntEnum):
    EIGHT_PAGE_MINI = 8
    QUARTER = 4
    HALF = 2


class PrintPage(MixableNamedTuple, Page):
    layout: Layout
    page: Page
    source_pages: tuple["FinalSheetSpread", ...]

    """
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
        self, dest_page: PrintPage, rect: Rect, scale: float | None = None
    ) -> tuple[str, str]:
        left_rect = Rect(rect.position, Size(rect.width / 2, rect.height))
        right_rect: Rect = Rect(
            Coord(rect.position.x + rect.width / 2, rect.position.y),
            left_rect.size,
        )

        return (
            self._translate_page(self.left, dest_page, left_rect, scale=scale),
            self._translate_page(
                self.right, dest_page, right_rect, scale=scale
            ),
        )

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
        source_objects = scribus.getAllObjects(page=source_page)
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
    inside: FinalSheetSpread
    outside: FinalSheetSpread


class FinalPageSource(enum.Enum):
    FRONT_START = enum.auto()
    FRONT_END = enum.auto()
    BACK_START = enum.auto()
    BACK_END = enum.auto()


class TranslatePosition(NamedTuple):
    page: int
    position: int


class FinalDoc(NamedTuple):
    layout: Layout
    pages: int
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
    def signature_pages(self) -> int:
        return self.signature_sheets * 4

    @property
    @lru_cache
    def signatures(self) -> int:
        if self.pages % (self.signature_pages):
            raise IncorrectNumberOfPages(
                f"{self.pages} is not divisible by {self.signature_pages} (the number of sheets in signatures * 4)"
            )
        return self.pages // self.signature_pages

    @property
    @lru_cache
    def cols(self) -> int:
        return self.layout // 4

    @property
    @lru_cache
    def rows(self) -> int:
        return self.layout // 2

    @property
    @lru_cache
    def print_pages(self) -> list[PrintPage]:
        front_pages: list[int] = list(range(1, self.pages + 1))  #  + [-1]
        split_idx = self.pages // 2
        front_pages, back_pages = (
            front_pages[:split_idx],
            front_pages[split_idx:],
        )
        print_pages: list[PrintPage] = []
        print(f"front_pages: {front_pages}\nback_pages:{back_pages}")
        while front_pages:
            front_spreads: list[FinalSheetSpread] = []
            back_spreads: list[FinalSheetSpread] = []
            for _ in range(self.rows):
                if not front_pages:
                    assert not back_pages
                    warn("breaking in rows")
                    break
                for _ in range(self.cols):
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

            if not isinstance(self.print_page_size, Size):
                raise ValueError(f"Wrong Size(): {self.print_page_size}")
            print_pages.extend(
                [
                    PrintPage(
                        self.layout,
                        Page(len(print_pages) + 1, size=self.print_page_size),
                        source_pages=tuple[FinalSheetSpread, ...](
                            front_spreads
                        ),
                    ),
                    PrintPage(
                        self.layout,
                        Page(len(print_pages) + 2, size=self.print_page_size),
                        source_pages=tuple[FinalSheetSpread, ...](back_spreads),
                    ),
                ]
            )

        for print_pg in range(
            self.pages // self.layout + (1 if self.pages % self.layout else 0)
        ):
            print(print_pg)

        return print_pages

    def assemble(
        self,
        new_name: str | Path | None = None,
        suffixer: Callable[[str | Path], Path] = default_suffixer,
    ):
        scribus.saveDoc()

        if new_name is None:
            new_name: Path = suffixer(scribus.getDocName())
        # Ensure new_name is a path object
        new_name = Path(new_name)
        assert new_name != Path(scribus.getDocName())
        """
        try:
            scribus.setPageSize(self.print_page_size)
        except AttributeError as exc:
            # pre 1.7 scribus
            raise EnvironmentError(f"pre 1.7 scribus, could not resize page in script (scribus version is {scribus.SCRIBUS_VERSION_INFO})") from exc
        """
        scribus.setDocType(scribus.NOFACINGPAGES, scribus.FIRSTPAGELEFT)
        scribus.saveDocAs(str(new_name))

        page_dims: dict[int, tuple[float, float]] = dict[
            int, tuple[float, float]
        ](
            (page_no, scribus.getPageNSize(page_no))
            for page_no in range(scribus.pageCount())
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
                    print_page,
                    Rect(Coord(x, y), Size(col_width, row_height)),
                )
                # Setup for next spread
                if col == self.cols - 1:
                    row += 1
                    col = 0
                    x = self.margins.left
                    y += row_height
                else:
                    col += 1
                    x += col_width


def _send_objects_to_layer(
    layer_name: str, send_objects: list[str], create: bool = False
):
    for send_object in send_objects:
        _send_to_layer(layer_name, send_object, create=create)


def _send_to_layer(
    layer_name: str, send_object: str | None = None, create: bool = False
) -> bool:
    if send_object is not None:

        def do_send(layer: str):
            return scribus.sendToLayer(layer, send_object)

    else:
        do_send: Callable[[str], None] = scribus.sendToLayer
    try:
        do_send(layer_name)
    except (scribus.NotFoundError, scribus.ScribusException) as exc:
        if create:
            # Layer not found, create it
            scribus.createLayer(layer_name)
            do_send(layer_name)
        else:
            raise exc


def _generate_pages(
    layout: Layout,
    total_pages: int,
    signature_size: int = 1,
    pad: bool = False,
    offset_start=1,
):
    """
    just brute force it for now
    """
    if not pad and total_pages % layout:
        # TODO
        raise ValueError()
    source_pages: list[int] = list(range(1, total_pages + 1))
    page_count = total_pages / layout
    pages = dict()
    i = 0
    sides = [
        list(
            range(
                (i * signature_size) * int(layout),
                ((i + 1) * signature_size) * int(layout),
            )
        )
        for i in range(total_pages // (signature_size * int(layout)))
    ]
    # TODO \/
    sheets = [Sheet(inside, outside) for inside, outside in []]
    print(sheets)
    return
    while source_pages:
        sig_pages: int = signature_size * int(layout)
        sig_offset: int = int(layout * signature_size + (i * layout))
        sig_start: int = total_pages // 2 - sig_offset
        sig_end: int = total_pages // 2 + sig_offset
        i += 1

        start = total_pages // 2 - int(layout // 2 + (i * layout))
        end: int = total_pages // 2 + int(layout // 2 + (i * layout))
        to_use = source_pages[sig_start:sig_end]
        source_pages = source_pages[:start] + source_pages[end:]
        for pos, source in enumerate(to_use):
            pages[source] = TranslatePosition(total_pages - i, pos)
        page_count -= int(layout)

        print("pages", start, end)
        print(pages)
        print(source_pages)


if __name__ == "__main__":
    print(_generate_pages(Layout.QUARTER, total_pages=16))

    doc = FinalDoc(Layout.QUARTER, 2, 16)
    print(doc)
    print(doc.print_pages)


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
        layout=layout,
        signature_sheets=signature_sheets,
        pages=page_count,
        print_page_size=Size.factory(*paper_size),
    )

    print_doc.assemble()


class IncorrectNumberOfPages(Exception):
    pass
