import dataclasses
import typing
from _typeshed import Incomplete
from logging import DEBUG as DEBUG, INFO as INFO
from typing import NamedTuple

logger: Incomplete
SCREEN_RE: Incomplete
DISP_RE: Incomplete
MODE_RE: Incomplete

class Dims(NamedTuple):
    x: Incomplete
    y: Incomplete

class _Rate(NamedTuple):
    rate: Incomplete
    active: Incomplete
    preferred: Incomplete

class Rate(_Rate):
    def __init__(self, rate: float, active: bool = False, preferred: bool = False) -> None: ...

@dataclasses.dataclass
class Mode:
    dims: Dims
    refresh_rates: list[Rate]
    PREFIX_RE: typing.ClassVar = ...
    MODE_RE: typing.ClassVar = ...
    REFRESH_RE: typing.ClassVar = ...
    @classmethod
    def parse(cls, in_str: str) -> Mode: ...
    @classmethod
    def parse_many(cls, in_str: str) -> typing.Iterator['Mode']: ...

@dataclasses.dataclass
class Display:
    name: str
    connected: bool
    primary: bool = ...
    active_conf: str = ...
    stuff: str = ...
    size: tuple[int, int] = ...
    modes: list[Mode] = dataclasses.field(default_factory=list)

def query(verbose: bool = False): ...
def parse(verbose: bool = False): ...
def main() -> None: ...
