from typing import NamedTuple
from pathlib import Path


def get_doc_page_sizes_and_margins():
    sizes = set()
    for pg in range(1, scribus.pageCount() + 1):
        sizes.add((scribus.getPageNSize(pg), scribus.getPageNMargins(pg)))
    return sizes


def get_doc_page_size_and_margins():
    sizes = get_doc_page_sizes_and_margins()
    if len(sizes) != 1:
        raise ValueError("Doc pages must be same size")
    return sizes.pop()


class CopySrc(NamedTuple):
    filename: str
    page: int


class CopyDest(NamedTuple):
    filename: str
    page: int


def copy_items(source: CopySrc, dest: CopyDest, offset=None):
    print(f"Copying from {source} to {dest}")
    scribus.openDoc(source.filename)
    scribus.gotoPage(source.page)
    pg_items = scribus.getPageItems()
    scribus.copyObjects([pi[0] for pi in pg_items])
    scribus.openDoc(dest.filename)
    scribus.gotoPage(dest.page)
    pasted = scribus.pasteObjects()
    if offset is not None:
        for po in pasted:
            scribus.moveObject(*offset, po)


def create_pages(
    source=None,
    dest="-spreads",
    front_cover=True,
    back_cover=True,
    pad_spreads=False,
    dest_is_suffix=True,
):
    if source is not None:
        scribus.openDoc(source)
    unit = scribus.getUnit()
    offset = int(front_cover)
    back_offset = int(back_cover)
    spread_sources = list(range(1, scribus.pageCount() + 1))
    if len(spread_sources) % 2 and not pad_spreads:
        raise ValueError("odd pages")
    source_size, source_margins = get_doc_page_size_and_margins()
    if dest_is_suffix:
        sourceP = Path(source)
        dest = str(sourceP.with_name(sourceP.stem + dest + sourceP.suffix))
    scribus.newDocument(
        (source_size[0] * 2, source_size[1]),
        source_margins,
        scribus.PORTRAIT,
        1,
        unit,
        scribus.PAGE_1,
        0,
        offset,
    )
    scribus.saveDocAs(dest)
    scribus.setDocType(scribus.NOFACINGPAGES, scribus.FIRSTPAGELEFT)
    print("boop")
    print(
        spread_sources[::2],
        spread_sources[1::2],
        range(len(spread_sources) // 2),
    )
    print(f"rangeval: {len(spread_sources) // 2}")
    print(
        list(
            (
                list(range(1 + offset, 2 + (len(spread_sources) // 2))),
                spread_sources[::2],
                spread_sources[1::2],
            )
        )
    )
    print(
        list(
            zip(
                range(1 + offset, 2 + (len(spread_sources) // 2)),
                spread_sources[::2],
                spread_sources[1::2],
            )
        )
    )
    for new_page, left_source, right_source in zip(
        range(1 + offset, 2 + ((len(spread_sources)) // 2)),
        spread_sources[offset::2],
        spread_sources[offset + 1 :: 2],
    ):
        print((new_page, left_source, right_source))
        scribus.newPage(new_page)
        copy_items(CopySrc(source, left_source), CopyDest(dest, new_page))
        copy_items(
            CopySrc(source, right_source),
            CopyDest(dest, new_page),
            (source_size[0], 0),
        )
    # Do covers
    if front_cover:
        copy_items(CopySrc(source, 1), CopyDest(dest, 1))
        if scribus.getDocName() != dest:
            print(f"Have to go to new doc")
            scribus.openDoc(dest)
        scribus.gotoPage(1)
        print(f"before set page size: {scribus.getPageSize()} to {source_size}")
        print(
            f"setting front cover size. {scribus.currentPage()}:{scribus.getDocName()}"
        )
        scribus.setCurrentPageSize(*source_size)
        print(f"after set page size: {scribus.getPageSize()}")
    if back_cover:
        scribus.newPage(-1)
        copy_items(
            CopySrc(source, spread_sources[-1]),
            CopyDest(dest, scribus.pageCount()),
        )
        if scribus.getDocName() != dest:
            print(f"Have to go to new doc")
            scribus.openDoc(dest)
        scribus.gotoPage(scribus.pageCount())
        scribus.setCurrentPageSize(*source_size)
    assert scribus.getDocName() != source
    scribus.saveDoc()


create_pages(
    r"C:\Users\me\zines\time_travellers_guide_resisting_extremism\zine.sla"
)


print([i for i in dir(scribus) if "page" in i.lower()])
