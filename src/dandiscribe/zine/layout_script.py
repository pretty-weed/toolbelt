from argparse import ArgumentParser, Namespace
import importlib
import sys

print(sys.path)
print(sys.version_info)
print(sys.executable)

# test_pages-n.sla has n pages, including front and back cover.
TEST_SOURCE_8 = "/home/dandelion/zines/test_pages-8.sla"
TEST_SOURCE_12 = "/home/dandelion/zines/test_pages-12.sla"
TEST_SOURCE_16 = "/home/dandelion/zines/test_pages-16.sla"

if "/usr/share/scribus/scripts" not in sys.path:
    sys.path.append("/usr/share/scribus/scripts")
from dandiscribe import script_utils

importlib.reload(script_utils)
script_utils.reload()
from dandiscribe.zine import layout as zine_layout
from dandiscribe.zine.layout import FinalDoc


def test_layouts(
    keep_source_open: bool = False, keep_final_open: bool = False
) -> None:
    # zine_layout.create_from_current_doc(zine_layout.Layout.QUARTER)

    close_source = not keep_source_open
    close_final = not keep_final_open

    print("half pages")
    doc1_2: FinalDoc = FinalDoc(
        "/home/dandelion/zines/test_res_half.sla", 2, zine_layout.Layout.HALF
    )
    doc1_2.assemble(
        TEST_SOURCE_8, close_source=close_source, close_final=close_final
    )
    print("quarter pages")
    doc1_4: FinalDoc = FinalDoc(
        "/home/dandelion/zines/test_res_quarter.sla",
        8,
        zine_layout.Layout.QUARTER,
    )
    doc1_4.assemble(
        TEST_SOURCE_12, close_source=close_source, close_final=close_final
    )
    print("8888888888888")
    doc1_8: FinalDoc = FinalDoc(
        "/home/dandelion/zines/test_res_eight.sla",
        4,
        zine_layout.Layout.EIGHT_PAGE_MINI,
    )
    doc1_8.assemble(
        TEST_SOURCE_8, close_source=close_source, close_final=close_final
    )

    # doc16: FinalDoc = FinalDoc("/home/dandelion/zines/test_res_half.sla", 8, zine_layout.Layout.HALF)
    # doc16.assemble(TEST_SOURCE_16)


def main() -> None:
    parser = ArgumentParser()
    _ = parser.add_argument("--keep_source_open", "--KS", action="store_true")
    _ = parser.add_argument("--keep_final_open", "--KF", action="store_true")
    parsed: Namespace = parser.parse_args()
    test_layouts(**vars(parsed))


if __name__ == "__main__":
    main()
