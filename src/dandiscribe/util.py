from collections.abc import Generator
from contextlib import contextmanager

from functools import partial
import logging
from logging import handlers
from os import getenv
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Generic, NamedTuple, TypeVar, override

from annotated_types import T
from dandiscribe.enums import Unit
from dandiscribe.exceptions import NoSuchMasterPage, WrongPageError
from dandiscribe.scribus_data import ScribusItem
from dandy_lib.datatypes.twodee import Number, Coord, Rect as Rect2d
from platformdirs import user_cache_dir

from numpy import array, matrix
import yaml

from dandiscribe.data import Rect, Size
from dandiscribe.log import configure
import scribus

LOG_DIR = Path(
    getenv("LOG_DIR", Path.home().joinpath(".local", "var", "log", "python"))
)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)
LOG_FILE = Path(
    getenv("LOG_FILE", LOG_DIR.joinpath(__name__).with_suffix(".log"))
)

LOGGER: logging.Logger = configure(__name__)

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


Tmp = TypeVar("Tmp")


class TempGoToBase(Generic[Tmp]):

    def __init__(self, page: Tmp):
        self.page: Tmp = page
        self.current: Tmp | None = None

    def _get_goto_page(self, go_back: bool = False) -> Tmp:
        if go_back:
            if self.current is None:
                raise ValueError("Cannot go back if current is not set")
            return self.current
        return self.page

    def _goto_page(self, go_back: bool = False) -> None:
        raise NotImplementedError("_goto_page must be implemented")

    def _go_back(self) -> None:
        self._goto_page(True)

    def __enter__(self):
        # todo handle returning to master pages
        self._goto_page()
        if self.current == self.page:
            LOGGER.debug(
                "%s GOTO current: %i , goto: %i", self, self.current, self.page
            )
            raise WrongPageError()
        return self.current

    def __exit__(
        self, type: type[Exception], value: Exception, traceback: TracebackType
    ):
        if self.current != self.page:
            LOGGER.debug(
                "%s EXIT current: %i , goto: %i", self, self.current, self.page
            )
            self._go_back()


class TempGoto(TempGoToBase[int]):

    @override
    def _goto_page(self, go_back: bool = False) -> None:
        go_page: int = self._get_goto_page(go_back)

        scribus.gotoPage(go_page)


class TempGoToMaster(TempGoToBase[str]):

    @override
    def _goto_page(self, go_back: bool = False) -> None:
        go_page: str = self._get_goto_page(go_back)

    @override
    def _go_to(self) -> None:
        return super()._go_to()


class EditMaster:
    stack: list[str] = []

    def __init__(self, name: str, create: bool = False) -> None:
        self.name = name
        exists = self.name in scribus.masterPageNames()
        if create and not exists:
            scribus.createMasterPage(self.name)
        elif not exists:
            raise NoSuchMasterPage(self.name)

    def __enter__(self) -> str:
        LOGGER.debug(
            "entering %s, current stack: [%s]",
            self.__class__,
            ", ".join(self.stack),
        )
        if self.stack:
            LOGGER.debug(
                "closing current master page. expect that it is %s",
                self.stack[-1],
            )
            scribus.zoomDocument(20.0)
            scribus.closeMasterPage()

            LOGGER.debug(
                "Closed master page %s (theoretically)", self.stack.pop(-1)
            )

            if self.stack:
                msg = f"expect that it is {self.stack[-1]}"
            else:
                msg = "expect no active master page"

        self.stack.append(self.name)
        return self.name

    def __exit__(
        self, type: type[Exception], value: Exception, traceback: TracebackType
    ):
        scribus.closeMasterPage()
        self.stack = self.stack[:-1]
        if self.stack:
            scribus.editMasterPage(self.stack[-1])


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


def get_master_page_items(name: str) -> list[ScribusItem]:
    with TempGoToMaster(name):
        return [ScribusItem.create(item) for item in scribus.getPageItems()]


def copy_items(
    source: CopySrc,
    dest: CopyDest,
    source_box: Rect | None = None,
    target_box: Rect | None = None,
    debug_boxes: bool = False,
) -> str:
    LOGGER.info(f"Copying from {source} to {dest}")

    # Set up some vars
    tempPage = f"temp-{source.page}->{dest.page}"
    group_name: str = f"page {source.page}"
    ibounds_name: str = f"bounds {source.page}"

    scribus.openDoc(source.filename)
    try:
        scribus.gotoPage(source.page)
    except IndexError as exc:
        raise IndexError(
            f"Failed going to page {source.page} in doc {scribus.getDocName()}"
        ) from exc
    if source_box is None:
        LOGGER.debug("No source box passed to copy_items, creating it")
        # ToDo: maybe (optionally)? consider margins
        source_box = Rect(
            position=Coord(0, 0),
            size=Size(
                *scribus.getPageNSize(source.page), Unit.get_current()
            ).as_points(),
        )
        LOGGER.debug(
            "no source box passed to `copy_items(), generated one: %s in %s",
            source_box,
            scribus.getDocName(),
        )

    invisible_bounds: str = source_box.create(name=ibounds_name)
    pg_items: list[str] = [pi[0] for pi in scribus.getPageItems()]
    scribus.copyObjects(pg_items)
    scribus.openDoc(dest.filename)
    scribus.createMasterPage(tempPage)
    if target_box is None:
        LOGGER.debug("No target box passed to copy_items, creating it")
        target_box = Rect(
            Coord(0, 0),
            Size(
                *scribus.getPageNSize(dest.page),
            ).as_points(),
        )
        LOGGER.debug(
            "no target box passed to `copy_items()`, generated one: %s in %s",
            target_box,
            scribus.getDocName(),
        )
    if debug_boxes:
        LOGGER.debug("creating debug rect %s", target_box)
        _ = scribus.createRect(
            target_box.x,
            target_box.y,
            target_box.width,
            target_box.height,
            f"debug-{source.page}->{dest.page}",
        )
    LOGGER.debug(
        "source dims: %s, target dims: %s", source_box.size, target_box.size
    )
    with EditMaster(tempPage):
        pasted = scribus.pasteObjects()
        for p_obj in pasted:
            # getItemPageNumber seems to be zero indexed?
            if scribus.getItemPageNumber(p_obj) != dest.page - 1:
                msg = (
                    f"{p_obj} not on correct page number (is "
                    f"{scribus.getItemPageNumber(p_obj)}, expected {dest.page - 1})"
                    f"(on {scribus.currentPageNumber()})"
                )

                try:
                    raise ValueError(msg)
                except ValueError:
                    LOGGER.exception(msg)
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
        # allow up to 5% skew adjust
        if not min(scale) / max(scale) > 0.95:

            msg = f"Not designed to skew scale yet ({scale} ({max(scale) / min(scale) * 100.0}% skew)) target box: {target_box}, source box: {source_box}"
            raise ValueError(msg)
        translate: tuple[Number, ...] = tuple[Number, ...](
            t - o for t, o in zip(target_box.position, (0, 0))
        )
        LOGGER.debug(
            "before rename, page items: %s",
            ", ".join(str(item) for item in scribus.getPageItems()),
        )
        pgroup = scribus.setNewName(group_name, scribus.groupObjects(pasted))
        LOGGER.debug(
            "after group and rename, pgroup is %s, group name is %s\npage items: %s",
            group_name,
            pgroup,
            ", ".join(str(item) for item in scribus.getPageItems()),
        )
        try:
            scribus.scaleGroup(min(scale), pgroup)
        except scribus.NoValidObjectError:
            LOGGER.exception("%s not found when scaling group", pgroup)
            assert pgroup in scribus.getPageItems()
        LOGGER.debug(
            "Moving %s by %s, scaling by %d", pgroup, translate, scale[0]
        )
        scribus.moveObject(translate[0], translate[1], pgroup)
        return pgroup


ok_to_ignore_dialog = _OkToIgnoreDialog()
