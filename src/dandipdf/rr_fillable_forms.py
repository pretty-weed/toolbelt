"""
Tool to generate fillable form fields for Root and Reckon training PDFs.
"""

import argparse
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
import re
from typing import Any
from yaml import safe_load

RANGERE = re.compile(r"(\d+)(-\d+|\+|(?:,\d+)+)?$")
import dandy_lib
import dandy_lib.geometry
from dandy_lib.cli.parser_types import path_exists

from dandy_lib.geometry import grid_from_segs

import fitz
from pymupdf import Page, Rect

from .util import stroke_to_seg


@dataclass
class Cell:
    w: float | int
    h: float | int


@dataclass
class Row:
    w: float | int
    h: float | int
    cells: list[Cell]


@dataclass
class Table:
    w: float | int
    h: float | int
    rows: list[Row]

    @classmethod
    def from_strokes(
        cls,
    ):
        pass


def draw_inputs(page: Page, spec: dict[str, dict[str, float]]):
    for name, input in spec.items():
        widget = fitz.Widget()
        widget.rect = Rect(
            input["x"],
            input["y"],
            input["x"] + input["width"],
            input["y"] + input["height"],
        )
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
        widget.field_name = name
        page.add_widget(widget)


def handle_drawing(drawing: dict[str, Any]):
    rect = drawing.get("rect")

    print(drawing)
    if rect is None:
        return

    # if rect.y1 - rect.y0 < 10:
    #    return

    print(
        f"x: {rect.x0}, y: {rect.y0}, width:{rect.width}, height: {rect.height}"
    )


def handle_page(pg: Page):
    print(pg)
    strokes = [
        stroke_to_seg(d) for d in pg.get_drawings() if d.get("type") == "s"
    ]
    import pprint

    pprint.pp(strokes)
    pprint.pp(grid_from_segs.find_rows(strokes))
    for drawing in pg.get_drawings():
        # if drawing["type"] in "sf":
        # if drawing["rect"] == pg.cropbox:
        #    continue
        handle_drawing(drawing)


def handle_doc(
    path: Path,
    out_dir: Path,
    pages: list[int] | None,
    spec: list[dict[str, dict[str, float]]] | None,
    suffix: str = "-input",
) -> None:
    doc = fitz.open(path)
    if pages is None:
        pages = list(range(1, len(doc) + 1))
    if len(pages) == 2 and pages[1] == float("inf"):
        # fill out the pages for this doc
        pages = list(range(pages[0], len(doc) + 1))
    print(f"pages: {pages}")
    for pg_i, page in enumerate(pages):
        if spec is not None and len(spec) >= pg_i:
            print(
                f"handling page {page} ({doc[page-1].rect}) from spec {spec[pg_i]}"
            )
            try:
                draw_inputs(doc[page - 1], spec[pg_i])
            except IndexError as exc:
                raise IndexError(
                    f"pg_i: {pg_i}, len(doc): {len(doc)}, len(spec): {len(spec)}"
                ) from exc
        else:
            print(f"non-spec handling page {page} ({doc[page-1]})")
            handle_page(doc[page - 1])
    out_fn = out_dir.joinpath(
        f"{path.with_suffix("").name}{suffix}"
    ).with_suffix(path.suffix)
    doc.save(str(out_fn))
    return doc


def page_range(in_val: str):
    res = RANGERE.match(in_val)
    if res is None:
        raise ValueError(f"{in_val} did not match {RANGERE}")
    first_val = int(res.group(1))
    match res.group(2)[0]:
        case "-":
            return list(range(first_val, int(res.group(2)[1:]) + 1))
        case ",":
            return [int(val) for val in in_val.split(",")]
        case "+":
            return [first_val, float("inf")]
        case _:
            return [first_val]


def handle_from_pdfs(parsed: argparse.Namespace):
    spec = None
    if parsed.yaml is not None:
        spec = safe_load(Path(parsed.yaml).read_text())
    for target in parsed.targets:
        handle_doc(target, parsed.out_dir, pages=parsed.pages, spec=spec)


def handle_from_yamls(parsed: argparse.Namespace):
    all_pdfs: set[Path] = set(
        chain.from_iterable(
            [
                (
                    [pp]
                    if pp.is_file()
                    else (
                        pp.rglob("*.pdf")
                        if pp.is_dir()
                        else Path(".").glob(str(pp))
                    )
                )
                for pp in [
                    Path(pdf_p)
                    for pdf_p in (
                        parsed.pdfs if parsed.pdfs is not None else ["."]
                    )
                ]
            ]
        )
    )

    print(f"All yamls: {parsed.targets}")

    for yaml_file in [Path(t) for t in parsed.targets]:
        print(f"👀 {yaml_file}")
        spec = safe_load(Path(yaml_file).read_text())
        pages = (
            parsed.pages if parsed.pages else page_range(spec.get("page_range"))
        )
        handled_pdfs: set[Path] = set()
        for pdf_re in [re.compile(raw_re) for raw_re in spec.get("file_match")]:
            print(f"🔎 {pdf_re}")
            handled_pdfs.update(
                [p for p in all_pdfs if pdf_re.match(p.with_suffix("").name)]
            )

        if len(handled_pdfs) != len(all_pdfs):
            print("Didn't handle these PDFS:")
            for nh in all_pdfs - handled_pdfs:
                print(f"   * {nh}")

        for pdf in handled_pdfs:
            print(f"Handling {pdf}")
            handle_doc(
                pdf,
                parsed.out_dir,
                pages=pages,
                suffix=parsed.suffix,
                spec=spec.get("input_boxen"),
            )


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(method=handle_from_yamls)
    # parser.add_argument("target_sizes", action="append", nargs=2)
    parent_parser = argparse.ArgumentParser(add_help=False)

    _ = parent_parser.add_argument("targets", type=path_exists, nargs="+")
    _ = parent_parser.add_argument("--pages", "--pg", "--p", type=page_range)
    _ = parent_parser.add_argument("--out_dir", type=Path, default=Path("."))
    _ = parent_parser.add_argument("--suffix", default="-inputs")
    subparsers = parser.add_subparsers(title="start")
    pdf_start_parser = subparsers.add_parser("pdf", parents=[parent_parser])
    pdf_start_parser.set_defaults(method=handle_from_pdfs)
    _ = pdf_start_parser.add_argument("--yaml")
    yaml_start_parser = subparsers.add_parser("yaml", parents=[parent_parser])
    yaml_start_parser.set_defaults(method=handle_from_yamls)
    _ = yaml_start_parser.add_argument("--pdfs", action="append")
    parsed = parser.parse_args()
    print(parsed)

    parsed.method(parsed)
