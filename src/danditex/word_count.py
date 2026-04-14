from argparse import ArgumentParser
from pathlib import Path
from pprint import pp
from TexSoup.tex import TexText
from yaml import safe_dump
from json import dumps
from TexSoup import TexSoup


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("docs", nargs="+")
    parser.add_argument(
        "--output", "-o", choices=["plain", "yaml", "json"], default="plain"
    )
    parsed = parser.parse_args()

    counts = {}

    for doc in parsed.docs:
        soup = TexSoup(Path(doc).read_text())

        to_count = "".join(
            [str(c) for c in soup.document.contents if isinstance(c, TexText)]
        )
        counts[doc] = len(to_count.split())

    if parsed.output == "plain":
        if len(parsed.docs) == 1:
            print(list(counts.values())[0])
        else:
            print("\n".join(f"{d}: {c}" for d, c in counts.items()))
    elif parsed.output == "yaml":
        print(safe_dump(counts))

    elif parsed.output == "json":
        print(dumps(counts))
    else:
        raise ValueError(f"unexpected output {parsed.output}")


if __name__ == "__main__":
    main()
