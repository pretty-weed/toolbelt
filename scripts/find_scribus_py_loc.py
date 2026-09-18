#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from pathlib import Path


def main() -> None:
    parser = ArgumentParser()
    _ = parser.add_argument("--all", "-a", action="store_true")
    _ = parser.add_argument(
        "--outfile", type=Path, default=Path("/tmp/scribus_py_path.txt")
    )
    _ = parser.add_argument("--quiet", "-q", action="store_true")
    parsed = parser.parse_args()

    matching = [entry for entry in sys.path if "scribus" in entry.lower()]

    if parsed.all:
        res = "\n".join(matching)

    else:
        # best guess, grab the first
        res = matching[0]
    if not parsed.quiet:
        print(res.strip())
    parsed.outfile.write_text(res.strip())
    sys.exit(0)


if __name__ == "__main__":
    main()
