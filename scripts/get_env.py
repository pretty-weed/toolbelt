import os
from pprint import pp
import sys


def pt(title: str) -> None:
    print(title_str(title, one_line=True)[0])


from dandiscribe.script_utils import title_str


def main() -> None:

    pt("Env Vars")
    pp(dict(os.environ))

    pt("Arguments")
    pp(sys.argv)

    pt("os dir")
    pp(dir(os))

    pt("sys dir")
    pp(dir(sys))

    pt("version info")
    pp(sys.version_info)
    pt("executable")
    pp(sys.executable)


if __name__ == "__main__":
    main()
