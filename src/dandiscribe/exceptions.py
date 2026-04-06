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
    def __init__(name: str) -> None:
        msg = f"could not find the master page {name}"
        self.name = name
        super().__init__(msg)
