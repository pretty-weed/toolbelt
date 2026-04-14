"""
dandiscribe.log

logging setup for dandiscribe
"""

import logging
from logging import handlers
from os import getenv
from pathlib import Path
from typing import Any

LOG_DIR = Path(
    getenv("LOG_DIR", Path.home().joinpath(".local", "var", "log", "python"))
)
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)
LOG_FILE = Path(
    getenv("LOG_FILE", LOG_DIR.joinpath(__name__).with_suffix(".log"))
)

LOG_LEVEL: int = logging.getLevelNamesMapping()[
    getenv("LOG_LEVEL", "WARNING").upper()
]

LOGGER: logging.Logger = logging.getLogger(__name__)


def configure(name: str = None, level: int = LOG_LEVEL) -> logging.Logger:
    logger: logging.Logger
    if name is None:
        logger = LOGGER
    else:
        logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(handlers.RotatingFileHandler(LOG_FILE))

    return logger
