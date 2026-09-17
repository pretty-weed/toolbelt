import logging
from _typeshed import Incomplete
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dandiscribe.data import Rect as Rect, Size as Size
from dandiscribe.enums import Unit as Unit
from dandiscribe.exceptions import (
    NoSuchMasterPage as NoSuchMasterPage,
    WrongPageError as WrongPageError,
)
from dandiscribe.log import configure as configure
from dandiscribe.scribus_data import ScribusItem as ScribusItem
from dandy_lib.datatypes.twodee import Vector as Vector
from pathlib import Path
from types import TracebackType
from typing import Any, Generic, NamedTuple, Self, TypeAlias, TypeVar

LOG_DIR: Incomplete
LOG_FILE: Incomplete
LOGGER: logging.Logger

class _MissingType: ...

MISSING: _MissingType
type JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[
    str, "JSONValue"
]
type YAMLValue = dict[str, "YAMLValue"] | list[
    "YAMLValue"
] | str | int | float | bool | None

class CopyTransformation(NamedTuple):
    translation: Vector
    scale: Vector

TransformHandler: TypeAlias = Callable[
    [Rect, Rect, list[str]], dict[frozenset[str]]
]

def no_skew(source: Rect, dest: Rect, objects: list[str]) -> list[str]: ...

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
def save_sandwich(save_as: str | None = None) -> Generator[None]: ...

get_cache_dir: Incomplete
CACHE_FILE: Incomplete

class InvalidCache(BaseException):
    def __init__(
        self, cache_type: type, cache_val: Any, cache_file: Path
    ) -> None: ...

def get_cache_res(): ...
def get_cache_val(key: str, cache_res=None): ...
def cache_val(key: str, value, overwrite: bool = False): ...
def clear_cache_val(key: str): ...
def get_justify_adjustments(count: int, remainder: int) -> list[int]: ...

class NotInDebugger(Exception): ...
class DebuggerNotEnabled(NotInDebugger): ...

class Debug:
    def __new__(cls, name: str, enabled: bool = False) -> Self: ...
    name: Incomplete
    enabled: Incomplete
    level: int
    def __init__(self, name, enabled: bool = False) -> None: ...
    def enable(self, enabled: bool = True) -> None: ...
    def disable(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None: ...
    def set_break(self) -> bool: ...

Tmp = TypeVar("Tmp")

class TempGoToBase(Generic[Tmp]):
    page: Tmp
    current: Tmp | None
    def __init__(self, page: Tmp) -> None: ...
    def __enter__(self): ...
    def __exit__(
        self, type: type[Exception], value: Exception, traceback: TracebackType
    ): ...

class TempGoTo(TempGoToBase[int]): ...
class TempGoToMaster(TempGoToBase[str]): ...

class EditMaster:
    stack: list[str]
    name: Incomplete
    def __init__(self, name: str, create: bool = False) -> None: ...
    def __enter__(self) -> str: ...
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

def get_master_page_items(name: str) -> list[ScribusItem]: ...
def copy_items(
    source: CopySrc,
    dest: CopyDest,
    source_box: Rect | None = None,
    target_box: Rect | None = None,
    rotation: float | int | None = None,
    transform_hander: TransformHandler = ...,
) -> str: ...

ok_to_ignore_dialog: Incomplete
