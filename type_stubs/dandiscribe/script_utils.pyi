PAD: str
S: str

def reload() -> None: ...
def title_str(
    title: str,
    one_line: bool = False,
    wrap_width: int | None = 79,
    side: str = "#",
    top: str = "=",
    bot: str = "",
    inner: str = "-",
    outer: str = "=",
) -> list[str]: ...
