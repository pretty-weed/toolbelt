from collections import UserList
from collections.abc import Collection
from copy import deepcopy as deepcopy
from pprint import pformat as pformat, pp as pp
from typing import Self, override

class Wrap(float):
    def __new__(
        cls,
        x: float = 0.0,
        /,
        wrap_completion: float = 1.0,
        source_orbit: int = -1,
    ) -> Self: ...
    wrap_completion: float
    source_orbit: int | None
    def __init__(
        self,
        x: float = 0.0,
        /,
        wrap_completion: float = 1.0,
        source_orbit: int = -1,
    ) -> None: ...
    def split(self, at_length: float | int) -> tuple[Self, Self]: ...
    @property
    def complete(self) -> bool: ...
    @property
    def incomplete(self) -> bool: ...

class Wraps(UserList[Wrap]):
    def length(self) -> float: ...

class Orbit(Wraps):
    target_len: float | int | None
    orbit_num: int
    def __init__(
        self,
        initlist: Collection[Wrap] | None = None,
        /,
        orbit_num: int = -1,
        target_len: float | int | None = None,
    ) -> None: ...

class Ply(Wraps):
    orbits: set[int]
    def __init__(
        self,
        initlist: Collection[Wrap] | None = None,
        /,
        orbits: set[int] | None = None,
    ) -> None: ...
    def remainder(self) -> Wrap | None: ...
    @override
    def __len__(self) -> int: ...
    def wraps_by_orbit(self) -> dict[int | None, Wraps]: ...

def int_or_float(inval: str): ...
def get_ordinal_suffix(n: int): ...

class OrbitInit:
    start_l: float
    end_l: float
    rotations: int
    tail: float
    def __init__(
        self, start_l: float, end_l: float, rotations: float, tail: float = 0.0
    ) -> None: ...

def main() -> None: ...
