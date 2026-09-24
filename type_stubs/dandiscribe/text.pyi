from . import enums as enums
from _typeshed import Incomplete
from collections.abc import Generator
from typing import Any

EMOJI_PATTERN: Incomplete

def contains_emoji(text: str) -> bool: ...
def get_emoji_indices_and_len(text: str) -> Generator[tuple[int, int], Any]: ...
def handle_emoji(frame_name: str, emoji_font: enums.FontFaces = ...): ...
def insert_emoji(
    emoji: str,
    frame_name: str,
    pos: int = -1,
    emoji_font: enums.FontFaces = ...,
): ...
