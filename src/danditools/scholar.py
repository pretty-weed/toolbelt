from argparse import ArgumentParser
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from enum import member, Enum
from json import dumps, loads
from os import getenv
from pathlib import PurePath
from pprint import pformat
from time import sleep
from typing import Optional, ClassVar

from serpapi import search

from dandy_lib.cli.parser import add_output_force_overwrite_to_parser
from dandy_lib.cli.enums import CallableChoiceEnum, EnumAction

PER_PAGE = 20
TIMEOUT_RETRIES = 3


@dataclass
class Author:
    name: str


@dataclass
class PublicationInfo:
    summary: str = field(compare=False, repr=False)
    authors: list[Author]

    @classmethod
    def from_json_obj(cls, json_obj: dict) -> "PublicationInfo":
        authors = [Author(auth["name"]) for auth in json_obj.get("authors", [])]
        return cls(**(json_obj | {"authors": authors}))


@dataclass
class Result:
    title: str
    result_id: str  # Not sure if I should compare this or not
    pub_type: str = field(
        metadata={"danditools": {"scholar": {"source": "type"}}}
    )
    publication_info: PublicationInfo
    snippet: str = field(repr=False, compare=False, default="")
    inline_links: dict[str, str | dict[str, str | int]] = field(
        compare=False, repr=False, default_factory=list
    )

    position: int = field(compare=False, repr=False, default=None)
    link: str = field(compare=False, default=None)
    resources: list[dict[str, str]] = field(
        compare=False, default_factory=list, repr=False
    )

    EXPORT_KEYS: ClassVar[list[str]] = [
        "title",
        "result_id",
        "pub_type",
        "inline_links",
        "publication_info",
    ]

    @classmethod
    def from_json_obj(cls, json_obj) -> "Result":
        json_obj = deepcopy(json_obj)
        if "pub_type" not in json_obj:
            try:
                json_obj["pub_type"] = json_obj.pop("type")
            except KeyError:
                json_obj["pub_type"] = None
        json_obj["publication_info"] = PublicationInfo.from_json_obj(
            json_obj.pop("publication_info")
        )
        try:
            return cls(**json_obj)
        except TypeError as exc:
            import pdb

            pdb.set_trace()

            raise exc

    @classmethod
    def iter_from_results(cls, results, raw=False):
        for res in (results if raw else results["organic_results"]):
            yield Result.from_json_obj(res)

    def dump(self) -> dict:
        return dict(
            (k, v) for k, v in asdict(self).items() if k in self.EXPORT_KEYS
        )


def author_key(result: Result) -> list[str]:
    return [author.name for author in result.publication_info.authors]


def citations_key(result: Result) -> int:
    return result.inline_links.get("cited_by", {}).get("total", 0)


class SortMethods(CallableChoiceEnum):

    @member
    def author(
        results: list[Result],
        reverse: bool = False,
        subsorts: Optional[list["SortMethods"]] = None,
    ):
        # ToDo: SubSorts
        return sorted(results, reverse=reverse, key=author_key)

    @member
    def citations(
        results: list[Result],
        reverse: bool = False,
        subsorts: Optional[list["SortMethods"]] = None,
    ):
        return sorted(results, reverse=not reverse, key=citations_key)

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)


def handle_write(
    output: PurePath,
    results: list,
    previous: Optional[list] = None,
    sort: SortMethods | None = None,
):
    if previous:
        new_results = [result for result in results if result not in previous]
        if new_results != results:
            pass  # print(f"Duplicate results found: {pformat([res for res in results if res not in new_results])}")
        if not new_results:
            return

        try:
            results = previous + [r for r in results if r not in previous]
        except NameError as exc:
            import pdb

            pdb.set_trace()
            raise exc
    # import pdb
    # pdb.set_trace()
    if sort is not None:
        results = sort(results)
    output.write_text(dumps([result.dump() for result in results]))


def query():
    parser = ArgumentParser()
    parser.add_argument("query")
    add_output_force_overwrite_to_parser(parser)
    parser.add_argument("--api_key", default=getenv("SERPAPI_KEY"))
    parser.add_argument("--max_res", type=int)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument(
        "--sort", choices=SortMethods, type=SortMethods, action=EnumAction
    )
    parser.add_argument("--aggressive_write", "-W", action="count")
    parser.add_argument("--append_previous", "--AP", action="store_true")

    parsed = parser.parse_args()

    params = {
        "engine": "google_scholar",
        "q": parsed.query,
        "hl": "en",
        "num": str(PER_PAGE),
        "api_key": parsed.api_key,
    }

    all_results = []
    index = parsed.start
    results = None

    if parsed.append_previous and parsed.output.exists():
        previous_results = list(
            Result.iter_from_results(loads(parsed.output.read_text()), raw=True)
        )
    else:
        previous_results = []

    match parsed.aggressive_write:
        case 0:
            print_interval = -1
        case 1:
            print_interval = 5
        case 2:
            print_interval = 3
        case 3:
            print_interval = 1
        case _:
            print_interval = 1

    iterations = 0

    while results is None or results["pagination"]["next"]:

        page_params = params | {"start": str(index)}
        results = search(page_params)
        try:
            all_results.extend(Result.iter_from_results(results))
        except KeyError:
            for retry in range(TIMEOUT_RETRIES):
                print(f"Retrying: {retry} for page starting at {index}")
                if (
                    results["search_information"]["organic_results_state"]
                    == "Fully empty"
                ):
                    sleep(5)
                    results = search(page_params)
                    if "organic_results" in results:
                        all_results.extend(Result.iter_from_results(results))
                        break
            else:
                print(f"skipping page starting {index}")
        if parsed.aggressive_write and not iterations % print_interval:
            print("doing aggressive write")
            handle_write(
                parsed.output, all_results, previous_results, sort=parsed.sort
            )
        index += PER_PAGE
        if parsed.max_res and len(results) > parsed.max_res:
            break

        iterations += 1

    handle_write(parsed.output, all_results, previous_results, sort=parsed.sort)
