from argparse import ArgumentParser, Namespace
from copy import copy, deepcopy
from dataclasses import dataclass, field
from enum import auto, StrEnum
from functools import cache, wraps
from pathlib import Path, PurePath
from pydoc import Doc
from typing import Any, Callable, Iterator, NamedTuple, Self

from pypdf import PageObject, PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from src.dandiscribe.layout import Page


def copy_cache(to_dec, deep=True) -> Callable:

    copy_func = deepcopy if deep else copy

    @wraps(to_dec)
    @cache
    def decorated(*args, **kwargs):
        res = to_dec(*args, **kwargs)
        return copy_func(res)

    return decorated


def extant_path_type(source: str) -> PurePath:

    res = Path(source)
    if not res.exists():
        raise ValueError(f"{source} does not exist")

    return res


class Edge(StrEnum):
    LONG = auto()
    SHORT = auto()
    VERTICAL = auto()
    HORIZONTAL = auto()


@copy_cache
def get_pages(source: Path) -> list[PageObject]:
    reader = PdfReader(source)
    # Return a list, as `.pages is a VirtualList`
    return list(reader.pages)


class Vector2(NamedTuple):
    x: float
    y: float


class SplitRes(NamedTuple):
    offset: Vector2
    edge: Edge
    dims: "Dimensions"


class Dimensions(NamedTuple):
    # dims in pixels
    width: float
    height: float

    def split_on_edge(
        self, edge: Edge = Edge.LONG, out_edge: Edge | None = None
    ) -> SplitRes:
        """
        Out edge allows to specify the edge given in the output value, so that this can be used
        recursively
        """

        out_edge = edge if out_edge is None else out_edge
        match edge:
            case "long":
                if self.width == self.height:
                    raise ValueError(
                        "Can't split a square on a long or short edge"
                    )
                if self.width > self.height:
                    return self.split_on_edge(Edge.HORIZONTAL, out_edge)
                else:
                    return self.split_on_edge(Edge.VERTICAL, out_edge)
            case "short":
                if self.width == self.height:
                    raise ValueError(
                        "Can't split a square on a long or short edge"
                    )

                elif self.width > self.height:
                    return self.split_on_edge(Edge.VERTICAL, out_edge)
                else:
                    return self.split_on_edge(Edge.HORIZONTAL, out_edge)
            case "vertical":

                return SplitRes(
                    Vector2(0.0, self.height / 2.0),
                    out_edge,
                    self._replace(width=self.width, height=self.height / 2.0),
                )

            case "horizontal":
                return SplitRes(
                    Vector2(self.width / 2.0, 0.0),
                    out_edge,
                    self._replace(
                        width=self.width / 2.0, height=self.height / 2.0
                    ),
                )
            case _:
                raise ValueError(
                    f"{edge} is not a valid edge to split on (long, short, vertical, horizontal)"
                )

        assert False, "never get here"


class PageDimensions(NamedTuple):
    # dims in pixels
    width: float
    height: float
    page: PageObject
    ppi: int = 72
    page_num: int | None = None
    original_page_num: int | None = None

    @classmethod
    def create_from_page(
        cls, page: PageObject, page_num: int | None = None
    ) -> "PageDimensions":
        page.transfer_rotation_to_content()
        box = page.mediabox
        return cls(box.width, box.height, page=page, page_num=page_num)

    def get_dimensions(self) -> Dimensions:
        return Dimensions(self.width, self.height)

    def in_inches(self, ppi: int | None = None):
        if ppi is None:
            ppi = self.ppi
        return (self.width / ppi, self.height / ppi)

    def split_on_edge(
        self, writer: PdfWriter, edge="long"
    ) -> tuple["PageDimensions", "PageDimensions"]:
        split = self.get_dimensions().split_on_edge(edge)
        original_page_num = (
            self.original_page_num
            if self.original_page_num is not None
            else self.page_num
        )
        mb = self.page.mediabox

        left = self.page.mediabox.left
        bot = self.page.mediabox.bottom
        width = self.page.mediabox.width
        height = self.page.mediabox.height

        self.page.mediabox.lower_left = (
            left + split.offset.x,
            bot + split.offset.y,
        )
        self.page.mediabox.upper_right = (
            left + split.offset.x + split.dims.width,
            bot + split.offset.y + split.dims.height,
        )

        page_a = self.__class__(
            split.dims.width,
            split.dims.height,
            page=writer.add_page(self.page),
            ppi=self.ppi,
            page_num=self.page_num,
            original_page_num=original_page_num,
        )

        self.page.mediabox.lower_left = (left, bot)
        self.page.mediabox.upper_right = (
            left + split.dims.width,
            bot + split.dims.height,
        )

        page_b = self.__class__(
            split.dims.width,
            split.dims.height,
            page=writer.add_page(self.page),
            ppi=self.ppi,
            page_num=None if self.page_num is None else self.page_num + 1,
            original_page_num=original_page_num,
        )

        return (page_a, page_b)

    @classmethod
    def create_from_pages(
        cls, pages: list[PageObject]
    ) -> Iterator["PageDimensions"]:
        for page_num, page in enumerate(pages):
            yield cls.create_from_page(page, page_num=page_num)


def crop_page(
    page: PageObject, dims: PageDimensions, offset: Vector2 = Vector2(0.0, 0.0)
):
    left = page.mediabox.left + offset.x
    bottom = page.mediabox.bottom + offset.y
    page.mediabox = RectangleObject(
        (left, bottom, left + dims.width, bottom + dims.height)
    )

    return page


class CantDetermineDimensions(Exception):
    def __init__(self, possible_dimensions: list[Dimensions]):
        self.possible_dimensions = copy(possible_dimensions)
        if not possible_dimensions:
            msg = "No possible dimensions found"
        elif len(possible_dimensions) > 1:
            print(possible_dimensions)
            msg = f"Multiple possible dimensions found: {', '.join(str(dim) for dim in possible_dimensions)}"
        else:
            raise ValueError("possible dimensions shouldn't have one value")

        super().__init__(msg)


class DocDimensions(NamedTuple):
    first: Dimensions | None
    body: dict[Dimensions, list[PageDimensions]]
    last: Dimensions | None
    ordered_body: list[PageDimensions] | None = None

    def guess_best_dims(self, split_on_edge: Edge = Edge.LONG) -> SplitRes:
        if self.body:
            possible: list[SplitRes] = list(
                dim.split_on_edge(split_on_edge) for dim in self.body
            )
        else:
            possible = list(
                [
                    dim.split_on_edge(edge=split_on_edge)
                    for dim in (self.first, self.last)
                    if dim is not None
                ]
            )

        if len(possible) == 1:
            return possible[0]
        raise CantDetermineDimensions([sres.dims for sres in possible])

    def get_needs_split_or_crop(self, dims: Dimensions | None = None):
        """
        Get the page numbers from this document which need split or cropped
        """
        if dims is None:
            split = self.guess_best_dims()

    @classmethod
    def create(cls, source: Path) -> "DocDimensions":
        pages = list(PageDimensions.create_from_pages(get_pages(source)))
        first: PageDimensions | None = pages.pop(0)
        if pages:
            last = pages.pop(-1)
        else:
            last = None

        body_pages: dict[Dimensions, list[PageDimensions]] = {}
        for page_dim in pages:
            body_pages.setdefault(page_dim.get_dimensions(), []).append(
                page_dim
            )
        if first is not None and first.get_dimensions() in body_pages:
            body_pages[first.get_dimensions()].insert(0, first)
            pages.insert(0, first)
            first = None
        if last is not None and last.get_dimensions() in body_pages:
            body_pages[last.get_dimensions()].append(last)
            pages.append(last)
            last = None

        return cls(
            first.get_dimensions() if first is not None else None,
            body_pages,
            last.get_dimensions() if last is not None else None,
            ordered_body=pages,
        )


def split_and_merge(
    sources: list[Path],
    dest: Path,
    dims: Dimensions | None = None,
    rotation: int | None = None,
) -> PdfWriter:

    writer = PdfWriter()

    docs = dict((source, DocDimensions.create(source)) for source in sources)

    while dims is None:
        sizes: dict[SplitRes, list[DocDimensions]] = {}

        for doc in docs.values():
            try:
                doc_split = doc.guess_best_dims()
            except CantDetermineDimensions as exc:
                if len(exc.possible_dimensions) > 1:
                    # TODO Prompt for this
                    raise NotImplementedError()
            else:
                sizes.setdefault(doc_split, list[DocDimensions]()).append(doc)

        if len(sizes) == 1:
            doc_split = list(sizes.keys())[0]
            dims = doc_split.dims

    for source, source_dims in docs.items():
        pages = get_pages(source)
        if rotation is not None:
            for page in pages:
                page.rotate(rotation)
        if source_dims.first is not None:
            writer.add_page(pages.pop(0))
        if source_dims.ordered_body:
            for page in source_dims.ordered_body:
                # split each page by determined dims
                # TODO add control to edge
                page.split_on_edge(writer, Edge.LONG)

        if source_dims.last is not None:
            writer.add_page(pages.pop(-1))

    with dest.open("wb") as file_handle:
        writer.write(file_handle)

    return writer


def dims_type(in_val):
    return Dimensions(*in_val.split(","))


def _get_parsed() -> tuple[Namespace, ArgumentParser]:

    parser = ArgumentParser()
    parser.add_argument("--merged", action="store_true")
    parser.add_argument("--dims", type=dims_type)
    parser.add_argument("sources", nargs="+", type=extant_path_type)
    parser.add_argument("dest", type=Path)
    parser.add_argument(
        "--split_side", choices=["long", "short", "vertical", "horizontal"]
    )
    parser.add_argument("--rotation", type=int)

    parsed = parser.parse_args()

    return parsed, parser


def demo():
    parsed = _get_parsed()
    reader = PdfReader(parsed.sources[0])

    writer = PdfWriter()

    # Add page 1 from reader to output document, unchanged.
    writer.add_page(reader.pages[0])

    # Add page 2 from reader, but rotated clockwise 90 degrees.
    writer.add_page(reader.pages[1].rotate(90))

    # Add page 3 from reader, but crop it to half size.
    page3 = reader.pages[2]
    page3.transfer_rotation_to_content()
    left = page3.mediabox.left
    bot = page3.mediabox.bottom
    width = page3.mediabox.width
    page3.mediabox.lower_left = (
        page3.mediabox.left + (width / 2),
        page3.mediabox.bottom,
    )
    writer.add_page(page3)
    page3.mediabox.lower_left = (left, bot)
    page3.mediabox.upper_right = (left + width / 2, page3.mediabox.top)
    writer.add_page(page3)

    # Write to pypdf-output.pdf.
    with open("pypdf-output.pdf", "wb") as fp:
        writer.write(fp)


def split():

    parsed, parser = _get_parsed()

    if parsed.merged and len(parsed.sources) < 2:
        parser.error("`--merged` doesn't make sense with only one source")

    if parsed.merged or len(parsed.sources) == 1:
        split_and_merge(
            parsed.sources, parsed.dest, parsed.dims, rotation=parsed.rotation
        )
    else:
        for source in parsed.sources:

            split_and_merge(
                [source],
                parsed.dest.joinpath(source.name),
                parsed.dims,
                rotation=parsed.rotation,
            )


if __name__ == "__main__":
    split()
