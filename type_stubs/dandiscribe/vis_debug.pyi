from collections.abc import Callable as Callable, Generator
from contextlib import contextmanager
from typing import Any

DEBUG_LAYER: str

def get_debug_layer(ensure_visible: bool = False) -> str: ...
@contextmanager
def debug_layer() -> Generator[None]: ...
def vis_log(
    do_log: Callable[..., list[str] | None],
    log_args: list[Any] | None = None,
    log_kwargs: dict[str, Any] | None = None,
    level: int = ...,
) -> list[str] | None: ...
def vis_debug(
    do_log: Callable[..., list[str] | None],
    log_args: list[Any] | None = None,
    log_kwargs: dict[str, Any] | None = None,
): ...
