from contextlib import contextmanager
from os import getenv

import debugpy
import scribus

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
    return getenv(env_var, "").lower() in ["true", "t", "yes", "sure", "i guess", "huyup"]



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
            self, 
            ignore_words=frozenset(
                ["cancel", "ignore", "no", "stop"])):
        self.ignore_words = ignore_words

    def __call__(self, title: str, message: str) -> str | object:
        if title in self._ignored:
            return IGNORED
        res = scribus.valueDialog(title, message)
        if res in self.ignore_words:
            self._ignored.add(title)

        return res

ok_to_ignore_dialog = _OkToIgnoreDialog() 

