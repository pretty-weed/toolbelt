from argparse import ArgumentParser
from typing import NamedTuple


class MultArg(NamedTuple):
    m: int
    pct: float

    def __mul__(self, other):
        return self.m * (0.01 * self.pct * other)

    def __rmul__(self, other):
        print(self, other)
        return self.__mul__(other)


def main():
    parser = ArgumentParser()
    parser.add_argument("dps", type=float)
    parser.add_argument("--multiple", "-M", nargs=2, action="append")

    parsed = parser.parse_args()

    print(parsed)
    print(parsed.dps + sum(parsed.dps * MultArg(*mv) for mv in parsed.multiple))


if __name__ == "__main__":
    main()
