from _typeshed import Incomplete
from shutil import ExecError as ExecError
from typing import Any

class NewDocError(Exception): ...
class InvalidSheet(Exception): ...

class NoObjects(Exception):
    doc: Incomplete
    page: Incomplete
    def __init__(self, document: str, page: int) -> None: ...

class WrongPageError(Exception):
    extra: dict[str, Any]
    def __init__(
        self,
        expected: int | str,
        actual: int | str,
        msg: str | None = None,
        **extra,
    ) -> None: ...

class NoSuchMasterPage(Exception):
    name: Incomplete
    def __init__(self, name: str) -> None: ...

class ScriptRunError(Exception):
    expected: Any | None
    actual: Any | None
    def __init__(
        self, msg: str, expected: Any | None = None, actual: Any | None = None
    ) -> None: ...

class PageOutOfRange(IndexError):
    page: Incomplete
    doc_name: Incomplete
    pages_added: Incomplete
    def __init__(
        self, page: int, doc_name: str = "", pages_added: int | None = None
    ) -> None: ...
    def added_pages(self) -> bool: ...
