import re
from collections.abc import Generator
from itertools import zip_longest
from typing import Any

import scribus

from . import enums

EMOJI_PATTERN = re.compile(
    r"([\U0001f300-\U0001f9ff\U0001fa00-\U0001faff\u2700-\u27bf]+)"
)


def contains_emoji(text: str) -> bool:
    """
    Returns True if the input text contains any emoji characters,
    otherwise returns False.
    """
    # Pattern matching common Unicode ranges for emojis, pictographs,
    # transport/map symbols, and dingbats
    return EMOJI_PATTERN.search(text) is not None


def get_emoji_indices_and_len(text: str) -> Generator[tuple[int, int], Any]:
    split = EMOJI_PATTERN.split(text)
    cursor = 0
    for plain, emoji in zip_longest(
        [split[i] for i in range(len(split))][::2],
        [split[i] for i in range(len(split))][1::2],
        fillvalue="",
    ):
        if not len(emoji):
            cursor += len(plain)
            continue
        yield cursor + len(plain), len(emoji)
        cursor += len(plain) + len(emoji)


def handle_emoji(
    frame_name: str, emoji_font: enums.FontFaces = enums.FontFaces.OPENMOJI
):
    for emj_start, emj_len in get_emoji_indices_and_len(
        scribus.getAllText(frame_name)
    ):
        scribus.selectText(emj_start, emj_len, frame_name)
        try:
            scribus.setFont(emoji_font, frame_name)
        except ValueError:
            import pprint

            pprint.pp(scribus.getFontNames())
            raise
    scribus.selectText(0, 0, frame_name)


def insert_emoji(
    emoji: str,
    frame_name: str,
    pos: int = -1,
    emoji_font: enums.FontFaces = enums.FontFaces.OPENMOJI,
):

    if pos < 0:
        pos = scribus.getTextLength(frame_name)
    scribus.insertText(emoji, pos, frame_name)
    emoji_length = len(emoji)
    scribus.selectText(pos, emoji_length, frame_name)
    scribus.setFont(emoji_font, frame_name)

    # Clear selection
    scribus.selectText(0, 0, frame_name)
