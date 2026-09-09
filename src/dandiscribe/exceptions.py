from shutil import ExecError
from typing import Any, LiteralString


class NewDocError(Exception):
    pass


class InvalidSheet(Exception):
    pass


class NoObjects(Exception):
    """
    Raise this when there are no objects for some action
    """

    def __init__(self, document: str, page: int):
        self.doc = document
        self.page = page
        super().__init__(f"No objects in doc {document} on page {page}")


class WrongPageError(Exception):
    def __init__(
        self,
        expected: int | str,
        actual: int | str,
        msg: str | None = None,
        **extra,
    ) -> None:

        self.extra: dict[str, Any] = extra or {}
        if msg is None:
            msg = f"On wrong page ({actual}) expected to be on {expected}"
        super.__init__(msg)


class NoSuchMasterPage(Exception):
    def __init__(self, name: str) -> None:
        msg = f"could not find the master page {name}"
        self.name = name
        super().__init__(msg)


class ScriptRunError(Exception):
    """
    Some unexpected situation arose when a script was running, which indicates
    that something expected did not happen
    """

    def __init__(
        self, msg: str, expected: Any | None = None, actual: Any | None = None
    ) -> None:
        self.expected: Any | None = expected
        self.actual: Any | None = actual

        return super().__init__(msg)


class PageOutOfRange(IndexError):
    def __init__(
        self, page: int, doc_name: str = "", pages_added: int | None = None
    ) -> None:

        self.page = page
        self.doc_name = doc_name
        self.pages_added = pages_added

        super().__init__(
            f"Page {page} is out of range{' in ' + doc_name if doc_name else ''}"
        )

    def added_pages(self) -> bool:
        return bool(self.pages_added)
