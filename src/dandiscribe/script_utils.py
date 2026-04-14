import importlib
import sys
from textwrap import wrap

PAD = S = " "

_LI = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


def reload() -> None:
    for name, mod in dict(sys.modules.items()).items():
        if name == "__name__":
            print(f"skipping reload of {name}")
            continue
        if name.startswith(("dandiscribe", "danditools", "dandy_lib")):

            importlib.reload(mod)


def title_str(
    title: str,
    one_line: bool = False,
    wrap_width: int | None = 79,
    side: str = "#",
    top: str = "=",
    bot: str = "",
    inner: str = "-",
    outer: str = "=",
) -> list[str]:
    l: str = side + PAD
    r: str = PAD + side
    if not bot:
        bot = top
    lines = title.splitlines()
    if one_line:
        if len(lines) != 1:
            raise ValueError(
                "title must have only one line (some text, no newlines)"
            )
        inner_title: str = f"{PAD + title + PAD:{inner}^{wrap_width//3}}"
        return [f"{inner_title:{outer}^{wrap_width}}"]
    if wrap_width:
        lines: list[str] = sum(
            [
                wrap(line, wrap_width - len(r) - len(l))
                for line in title.splitlines()
            ],
            [],
        )
    else:
        wrap_width = 80
    inner_width: int = wrap_width - len(l) - len(r)
    ret_lines: list = [top * wrap_width]
    return (
        [top * wrap_width]
        + [l + f"{line: <{inner_width}}" + r for line in lines]
        + [bot * wrap_width]
    )
