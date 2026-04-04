from _typeshed import Incomplete
from collections.abc import Generator
from contextlib import contextmanager
from dandy_lib.datatypes.numeric import (
    NonNegFloat as NonNegFloat,
    NonNegInt as NonNegInt,
    NonNegNum as NonNegNum,
)
from dandy_lib.datatypes.twodee import Rect
from numpy import array as array, matrix as matrix
from types import TracebackType
from typing import NamedTuple

LOG_DIR: Incomplete
LOG_FILE: Incomplete
LOGGER: Incomplete
MISSING: Incomplete

class PauseDrawing:
    @classmethod
    def __enter__(cls) -> None: ...
    @classmethod
    def __exit__(
        cls,
        type: type[BaseException],
        value: BaseException,
        traceback: TracebackType,
    ): ...

@contextmanager
def save_sandwich(
    save_as: str | None = None,
) -> Generator[None, None, None]: ...

get_cache_dir: Incomplete
CACHE_FILE: Incomplete

def get_cache_res() -> str | int | float | list | dict | None: ...
def get_cache_val(key: str, cache_res=None): ...
def cache_val(key: str, value, overwrite: bool = False): ...
def clear_cache_val(key: str): ...
def get_justify_adjustments(count: int, remainder: int) -> list[int]: ...

class NotInDebugger(Exception): ...
class DebuggerNotEnabled(NotInDebugger): ...

class TempGoTo:
    page: Incomplete
    current: int | None
    def __init__(self, page: int) -> None: ...
    def __enter__(self): ...
    def __exit__(
        self, type: type[Exception], value: Exception, traceback: TracebackType
    ): ...

IGNORED: Incomplete

class _OkToIgnoreDialog:
    ignore_words: Incomplete
    def __init__(self, ignore_words=...) -> None: ...
    def __call__(self, title: str, message: str) -> str | object: ...

class CopySrc(NamedTuple):
    filename: str
    page: int
    counted: bool = ...

class CopyDest(NamedTuple):
    filename: str
    page: int

def copy_items(
    source: CopySrc,
    dest: CopyDest,
    source_box: Rect | None = None,
    target_box: Rect | None = None,
    debug_boxes: bool = False,
) -> str: ...

ok_to_ignore_dialog: Incomplete
