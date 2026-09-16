import logging
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any

import scribus

import dandiscribe

DEBUG_LAYER = "debug"


def get_debug_layer(ensure_visible: bool = False) -> str:
    if DEBUG_LAYER not in scribus.getLayers():
        scribus.createLayer(DEBUG_LAYER)
    if ensure_visible and not scribus.isLayerVisible(DEBUG_LAYER):
        scribus.setLayerVisible(DEBUG_LAYER, True)
    return DEBUG_LAYER


@contextmanager
def debug_layer() -> Generator[None]:
    layer = get_debug_layer()
    active_layer = scribus.getActiveLayer()
    print(f"active layer is {active_layer}")
    if active_layer != layer:
        scribus.setActiveLayer(layer)
        try:
            yield
        finally:
            scribus.setActiveLayer(active_layer)
    else:
        yield


def vis_log(
    do_log: Callable[..., list[str] | None],
    log_args: list[Any] | None = None,
    log_kwargs: dict[str, Any] | None = None,
    level: int = logging.DEBUG,
) -> list[str] | None:
    """
    Do a visual "log" (debug) with one or more items
    """
    log_args = log_args or []
    log_kwargs = log_kwargs or {}
    if level > dandiscribe.VISUAL_DEBUG_LEVEL:
        print(
            f"Not doing visual debug, log level {dandiscribe.VISUAL_DEBUG_LEVEL} not high enough"
        )
        return None
    print("doing visual debug")
    with debug_layer():
        res = do_log(*log_args, **log_kwargs)

    return res


def vis_debug(
    do_log: Callable[..., list[str] | None],
    log_args: list[Any] | None = None,
    log_kwargs: dict[str, Any] | None = None,
):
    return vis_log(do_log, log_args, log_kwargs, level=logging.DEBUG)
