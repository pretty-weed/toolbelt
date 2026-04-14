import logging
from _typeshed import Incomplete

LOG_DIR: Incomplete
LOG_FILE: Incomplete
LOG_LEVEL: int
LOGGER: logging.Logger

def configure(name: str = None, level: int = ...) -> logging.Logger: ...
