from _typeshed import Incomplete
from collections.abc import Generator
from dandy_lib.cli.enums import CallableChoiceEnum
from dataclasses import dataclass, field
from enum import Enum as Enum, member
from pathlib import PurePath
from pprint import pformat as pformat
from typing import ClassVar

PER_PAGE: int
TIMEOUT_RETRIES: int

@dataclass
class Author:
    name: str

@dataclass
class PublicationInfo:
    summary: str = field(compare=False, repr=False)
    authors: list[Author]
    @classmethod
    def from_json_obj(cls, json_obj: dict) -> PublicationInfo: ...

@dataclass
class Result:
    title: str
    result_id: str
    pub_type: str = field(metadata={'danditools': {'scholar': {'source': 'type'}}})
    publication_info: PublicationInfo
    snippet: str = field(repr=False, compare=False, default='')
    inline_links: dict[str, str | dict[str, str | int]] = field(compare=False, repr=False, default_factory=list)
    position: int = field(compare=False, repr=False, default=None)
    link: str = field(compare=False, default=None)
    resources: list[dict[str, str]] = field(compare=False, default_factory=list, repr=False)
    EXPORT_KEYS: ClassVar[list[str]] = ...
    @classmethod
    def from_json_obj(cls, json_obj) -> Result: ...
    @classmethod
    def iter_from_results(cls, results, raw: bool = False) -> Generator[Incomplete]: ...
    def dump(self) -> dict: ...

def author_key(result: Result) -> list[str]: ...
def citations_key(result: Result) -> int: ...

class SortMethods(CallableChoiceEnum):
    @member
    def author(results: list[Result], reverse: bool = False, subsorts: list['SortMethods'] = None): ...
    @member
    def citations(results: list[Result], reverse: bool = False, subsorts: list['SortMethods'] = None): ...
    def __call__(self, *args, **kwargs): ...

def handle_write(output: PurePath, results: list, previous: list = None, sort: SortMethods | None = None): ...
def query() -> None: ...
