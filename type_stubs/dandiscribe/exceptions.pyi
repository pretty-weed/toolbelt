from _typeshed import Incomplete
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
