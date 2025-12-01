from contextlib import contextmanager
from functools import partial
from os import getenv
from pathlib import Path
from platformdirs import user_cache_dir

import yaml

try:
    import debugpy
except ImportError:
    # it's an extra
    pass

import scribus

MISSING = object()


class PauseDrawing:
    _level = 0

    @classmethod
    def __enter__(cls):
        # perhaps profile to see if I should remove this when not necesary
        scribus.setRedraw(False)
        cls._level += 1

    @classmethod
    def __exit__(cls, type, value, traceback):
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


class Debug:
    _debuggers = {}
    enabled = {}
    entered = {}

    def __new__(cls, debug_id: str, *args, **kwargs):
        if debug_id in cls._debuggers:
            return cls._debuggers[debug_id]
        return super().__new__(cls)

    def __init__(self, debug_id: str, enabled: bool | None = None):
        self.debug_id = debug_id
        if enabled is not None:
            self.enabled[debug_id] = enabled
        elif self.enabled.get(debug_id) is None:
            # set from env var
            self.enabled[debug_id] = _get_env_bool("DEBUG")

    def __enter__(self):
        if self.enabled.get(self.debug_id):
            debugpy.listen(8000)
            debugpy.wait_for_client()
        return self

    def __exit__(self, type, value, traceback):
        pass

    @contextmanager
    def do_break(self, required: bool = False):
        if not self.entered.get(self.debug_id):
            if required:
                raise NotInDebugger()
            return
        elif not self.enabled.get(self.debug_id):
            if reqiured:
                raise DebuggerNotEnabled()
            return

        debugpy.set_trace()
        yield


get_cache_dir = partial(user_cache_dir, "dandiscribe", "DandelionGood")
CACHE_FILE = Path(get_cache_dir()).joinpath("cache.yml")


def get_cache_res():
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
            justify_adjustments = [
                adj + remainder // rows for adj in justify_adjustments
            ]
            remainder = remainder % rows
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
        self.current = None

    def __enter__(self):
        self.current = scribus.currentPage()
        print(f"ENTER current: {self.current}, goto: {self.page}")
        if self.current != self.page:
            print(f"GOTO current: {self.current}, goto: {self.page}")
            scribus.gotoPage(self.page)
        return self.current

    def __exit__(self, type, value, traceback):
        if self.current != self.page:
            print(f"EXIT current: {self.current}, goto: {self.page}")
            scribus.gotoPage(self.current)


IGNORED = object()


class _OkToIgnoreDialog:
    _ignored = set()

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


ok_to_ignore_dialog = _OkToIgnoreDialog()
