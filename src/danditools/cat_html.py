import argparse
from pathlib import Path, PurePath
from typing import NamedTuple

from bs4 import BeautifulSoup

from dandy_lib.cli.parser_types import path_exists
from dandy_lib.cli.parser import add_output_force_overwrite_to_parser


def get_elements(
    soup: BeautifulSoup,
    tag: str | None = None,
    tag_id: str | None = None,
    tag_class: str | None = None,
    max_elements=None,
):
    if tag is None and tag_id is None and tag_class is None:
        res = soup.find_all("body")
        return res[0]

    find_kwargs = {}
    if tag is None:
        tag = True
    if tag_id is not None:
        find_kwargs["id"] = tag_id
    if tag_class is not None:
        find_kwargs["class_"] = tag_class

    results = soup.find_all(tag, **find_kwargs)
    if max_elements is not None and len(results) > max_elements:
        raise TypeError("Found too many elements")
    return results


class CleanupConf(NamedTuple):
    tag: str
    id: str
    class_: str
    first_page: bool = False
    remaining_pages: bool = True
    next_elements: list["CleanupConf"] | None = None

    def get_elements(self, element) -> list:
        raise NotImplementedError()


class AppendAssembled(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self.assembled_type = kwargs.pop("type")
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            getattr(namespace, self.dest).append(self.assembled_type(*values))
        except AttributeError:
            setattr(namespace, self.dest, [])
            return self(parser, namespace, values, option_string=option_string)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sorted", "--sort", action="store_true")
    parser.add_argument("--wrapper_tag")
    parser.add_argument("--wrapper_id")
    parser.add_argument("--wrapper_class")
    parser.add_argument(
        "--cleanup", action=AppendAssembled, type=CleanupConf, nargs=3
    )
    parser.add_argument("source_files", nargs="+", type=path_exists)
    add_output_force_overwrite_to_parser(parser)

    parsed = parser.parse_args()

    if parsed.sorted:
        parsed.source_files = sorted(parsed.source_files)

    if len(parsed.source_files) == 1:
        parsed.output.write_text(parsed.source_files[0].read_text())
        return

    result = BeautifulSoup(parsed.source_files[0].read_text())
    root = get_elements(
        result,
        parsed.wrapper_tag,
        parsed.wrapper_id,
        parsed.wrapper_class,
        max_elements=1,
    )[0]
    for cleanup in parsed.cleanup:
        if cleanup.first_page:
            for element in get_elements(
                root, cleanup.tag, cleanup.id, cleanup.class_
            ):
                element.extract()

    for source in parsed.source_files[1:]:
        this_soup = BeautifulSoup(source.read_text())
        this_root = get_elements(
            this_soup,
            parsed.wrapper_tag,
            parsed.wrapper_id,
            parsed.wrapper_class,
            max_elements=1,
        )[0]
        for child in this_root.find_all(True, recursive=False):
            extracted = child.extract()
            for cleanup in parsed.cleanup:
                if cleanup.remaining_pages:
                    for element in get_elements(
                        extracted, cleanup.tag, cleanup.id, cleanup.class_
                    ):
                        element.extract()
            root.append(extracted)

    parsed.output.write_text(result.prettify())


if __name__ == "__main__":
    main()
