from collections.abc import Generator
from contextlib import contextmanager
from dandy_lib.datatypes.numeric import NonNegFloat, NonNegInt, NonNegNum
from dandy_lib.datatypes.twodee import Number, Rect
from functools import partial
import logging
from os import getenv
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, NamedTuple
import dandy_lib.datatypes.twodee
from dandy_lib.datatypes.twodee import Coord, Size, Rect
from platformdirs import user_cache_dir

from numpy import array, matrix
import yaml

import scribus

LOG_DIR = Path(
    getenv("LOG_DIR", Path.home().joinpath(".local", "var", "log", "python"))
)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)
LOG_FILE = Path(
    getenv("LOG_FILE", LOG_DIR.joinpath(__name__).with_suffix(".log"))
)

LOGGER = logging.getLogger(__name__)
MISSING = object()


class PauseDrawing:
    _level = 0

    @classmethod
    def __enter__(cls):
        # perhaps profile to see if I should remove this when not necessary
        scribus.setRedraw(False)
        cls._level += 1

    @classmethod
    def __exit__(
        cls,
        type: type[BaseException],
        value: BaseException,
        traceback: TracebackType,
    ):
        if cls._level:
            cls._level -= 1
        if not cls._level:
            scribus.setRedraw(True)
            scribus.redrawAll()


def _get_env_bool(env_var: str):
    return getenv(env_var, "").lower() in [
        "true",
        "t",
        "yes",
        "sure",
        "i guess",
        "huyup",
    ]


@contextmanager
def save_sandwich(save_as: str | None = None) -> Generator[None, None, None]:
    if save_as:
        do_save: Callable[[], None] = partial(scribus.saveDocAs, save_as)
    else:
        do_save = scribus.saveDoc
    do_save()
    yield
    do_save()


get_cache_dir = partial(user_cache_dir, "dandiscribe", "DandelionGood")

CACHE_FILE = Path(get_cache_dir()).joinpath("cache.yml")


def get_cache_res() -> str | int | float | list | dict | None:
    if not CACHE_FILE.is_file():
        return MISSING
    return yaml.safe_load(CACHE_FILE.read_text())


def get_cache_val(key: str, cache_res=None):
    if cache_res is None:
        cache_res = get_cache_res()
    if cache_res is MISSING or not cache_res:
        return MISSING

    return cache_res.get(key, MISSING)


def cache_val(key: str, value, overwrite: bool = False):
    cache_res = get_cache_res()
    if cache_res is MISSING:
        cache_res = {}
    if (not overwrite) and get_cache_val(key, cache_res) is not MISSING:
        raise TypeError("Cannot overwrite cache without overwrite set True")
    cache_res[key] = value
    if not CACHE_FILE.parent.exists():
        CACHE_FILE.parent.mkdir()
    with CACHE_FILE.open("w") as file_handle:
        yaml.safe_dump(cache_res, file_handle)


def clear_cache_val(key: str):
    cache_res = get_cache_res
    if cache_res is MISSING:
        return
    if key in cache_res:
        del cache_res[key]
    else:
        return
    with CACHE_FILE.open("r") as file_handle:
        yaml.safe_dump(cache_res, file_handle)


def get_justify_adjustments(count: int, remainder: int) -> list[int]:
    justify_adjustments = [0] * count
    if not count:
        raise ValueError("Division by zero")
    while remainder:
        if remainder >= count:
            justify_adjustments: list[int] = [
                adj + remainder // count for adj in justify_adjustments
            ]
            remainder = remainder % count
        else:
            justify_adjustments[:remainder] = [
                rem + 1 for rem in justify_adjustments[:remainder]
            ]
            remainder = 0
    return justify_adjustments


class NotInDebugger(Exception):
    pass


class DebuggerNotEnabled(NotInDebugger):
    pass


class TempGoTo:
    def __init__(self, page: int):
        self.page = page
        self.current: int | None = None

    def __enter__(self):
        self.current = scribus.currentPage()
        LOGGER.debug(
            "%s ENTER current: %i , goto: %i", self, self.current, self.page
        )
        if self.current != self.page:
            LOGGER.debug(
                "%s GOTO current: %i , goto: %i", self, self.current, self.page
            )
            scribus.gotoPage(self.page)
        return self.current

    def __exit__(
        self, type: type[Exception], value: Exception, traceback: TracebackType
    ):
        if self.current != self.page:
            LOGGER.debug(
                "%s EXIT current: %i , goto: %i", self, self.current, self.page
            )
            scribus.gotoPage(self.current)


IGNORED = object()


class _OkToIgnoreDialog:
    _ignored: set[str] = set[str]()

    def __init__(
        self, ignore_words=frozenset(["cancel", "ignore", "no", "stop"])
    ):
        self.ignore_words = ignore_words

    def __call__(self, title: str, message: str) -> str | object:
        if title in self._ignored:
            return IGNORED
        res = scribus.valueDialog(title, str(message))
        if res in self.ignore_words:
            self._ignored.add(title)
        elif res == "clear":
            self._ignored.clear()

        return res


class CopySrc(NamedTuple):
    filename: str
    page: int
    counted: bool = True


class CopyDest(NamedTuple):
    filename: str
    page: int


def copy_items(
    source: CopySrc,
    dest: CopyDest,
    source_box: Rect | None = None,
    target_box: Rect | None = None,
    debug_boxes: bool = False,
) -> str:
    print(f"Copying from {source} to {dest}")
    scribus.openDoc(source.filename)
    scribus.gotoPage(source.page)
    if source_box is None:
        # ToDo: maybe (optionally)? consider margins
        source_box: Rect = Rect(
            position=Coord(0, 0), size=Size(*scribus.getPageNSize(source.page))
        )
    pg_items: list[str] = [pi[0] for pi in scribus.getPageItems()]
    scribus.copyObjects(pg_items)
    scribus.openDoc(dest.filename)
    tempPage = f"temp-{source.page}->{dest.page}"
    group_name: str = f"page {source.page}"
    scribus.createMasterPage(tempPage)
    scribus.editMasterPage(tempPage)
    if target_box is None:
        target_box = Rect(Coord(0, 0), Size(*scribus.getPageNSize(dest.page)))
    if debug_boxes:
        LOGGER.debug("creating debug rect %s", target_box)
        scribus.createRect(
            target_box.x,
            target_box.y,
            target_box.width,
            target_box.height,
            f"debug-{source.page}->{dest.page}",
        )
    pasted = scribus.pasteObjects()
    for p_obj in pasted:
        if scribus.getItemPageNumber(p_obj) != dest.page:
            raise ValueError(
                f"{p_obj} not on correct page number (is {scribus.getItemPageNumber(p_obj)},, expected {dest.page}) (on {scribus.currentPageNumber()})"
            )
        else:
            LOGGER.info(
                "%s is on correct page (%i). position: %s",
                p_obj,
                scribus.getItemPageNumber(p_obj),
                scribus.getPosition(p_obj),
            )
    # calc translations
    scale: tuple[float, float] = tuple[float, float](
        ts / os for ts, os in zip(target_box.size, source_box.size)
    )
    if not scale[0] == scale[1]:

        msg = f"Not designed to skew scale yet ({scale}) target box: {target_box}, source box: {source_box}"
        exc: ValueError = ValueError(msg)
        if True:
            try:
                raise exc
            except ValueError:
                LOGGER.exception(msg)

            scale = (min(scale),) * 2
        else:
            raise exc
    translate: tuple[Number, ...] = tuple[Number, ...](
        t - o for t, o in zip(target_box.position, (0, 0))
    )
    pgroup = scribus.setNewName(scribus.groupObjects(pasted))
    scribus.scaleGroup(scale[0], pgroup)
    for po in pasted:
        LOGGER.debug("Moving %s by %s, scaling by %d", po, translate, scale[0])
        scribus.moveObject(translate[0], translate[1], po)
    return pgroup


ok_to_ignore_dialog = _OkToIgnoreDialog()
