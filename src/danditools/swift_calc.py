from collections import UserList
from collections.abc import Collection
import pdb
from pprint import pformat, pp
from typing import Any, Self, override


import argparse
from copy import deepcopy

from dandy_lib.cli.parser_actions import NargsRangeAppendAction


class Wrap(float):
    def __new__(
        cls,
        x: float = 0.0,
        /,
        wrap_completion: float = 1.0,
        source_orbit: int = -1,
    ) -> Self:
        return super().__new__(cls, x)

    def __init__(self, x: float = 0.0, /, wrap_completion: float = 1.0, source_orbit: int = -1) -> None:  # type: ignore[override]
        self.wrap_completion: float = float(wrap_completion)
        self.source_orbit: int | None = (
            None if source_orbit < 0 else source_orbit
        )
        super().__init__()

    def split(self, at_length: float | int) -> tuple[Self, Self]:
        if at_length < 0:
            from_end = self + at_length
            if from_end < 0:
                raise ValueError(
                    f"Cannot split wrap of length {self} at {-at_length} from end"
                )
        if at_length > self:
            raise ValueError(f"Cannot split {self} at length {at_length}.")
        orbit = self.source_orbit if self.source_orbit is not None else -1
        return (
            self.__class__(at_length, at_length / self, orbit),
            self.__class__(self - at_length, (self - at_length) / self, orbit),
        )

    @property
    def complete(self) -> bool:
        return self.wrap_completion >= 1.0

    @property
    def incomplete(self) -> bool:
        return not self.complete

    @override
    def __str__(self) -> str:
        rep: str = f'<Wrap {self:.3f}" ({self.wrap_completion:.2%})'
        if self.source_orbit is not None:
            rep += f" from orbit {self.source_orbit}"
        return rep + ">"


class Wraps(UserList[Wrap]):

    def length(self) -> float:
        return sum(self)


class Orbit(Wraps):

    def __init__(
        self,
        initlist: Collection[Wrap] | None = None,
        /,
        orbit_num: int = -1,
        target_len: float | int | None = None,
    ) -> None:
        self.target_len: float | int | None = target_len
        self.orbit_num: int = orbit_num
        super().__init__(initlist)


class Ply(Wraps):
    def __init__(
        self,
        initlist: Collection[Wrap] | None = None,
        /,
        orbits: set[int] | None = None,
    ) -> None:
        self.orbits: set[int] = orbits or set[int]()
        super().__init__(initlist)

    def remainder(self) -> Wrap | None:
        if self[-1].complete:
            return None
        return self[-1]

    @override
    def __len__(self) -> int:
        """
        Don't include remainder in len
        """
        return super().__len__() - int(bool(self.remainder()))

    def wraps_by_orbit(self) -> dict[int | None, Wraps]:
        wraps: dict[int | None, Wraps] = {}
        for wrap in self:
            wraps.setdefault(wrap.source_orbit, Wraps()).append(wrap)
        return wraps


def int_or_float(inval: str):
    try:
        return int(inval)
    except ValueError:
        return float(inval)


def get_ordinal_suffix(n: int):
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


class OrbitInit:
    def __init__(
        self, start_l: float, end_l: float, rotations: float, tail: float = 0.0
    ) -> None:
        self.start_l: float = start_l
        self.end_l: float = end_l
        assert int(rotations) == rotations
        self.rotations: int = int(rotations)
        self.tail: float = tail


def main():

    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--ply", type=int, default=1)
    _ = parser.add_argument(
        "--orbit",
        dest="orbits",
        nargs=(3, 4),
        append_type=OrbitInit,  # type: ignore[arg-type]
        action=NargsRangeAppendAction,
        type=float,
    )
    parsed = parser.parse_args()

    total = 0.0
    orbits: list[Orbit] = []
    for orbit_i, orbit_setup in enumerate(parsed.orbits):
        start_l, end_l, rotations = (
            orbit_setup.start_l,
            orbit_setup.end_l,
            orbit_setup.rotations,
        )
        min_l, max_l = sorted([start_l, end_l])

        # assume a continuous distribution
        max_diff = max_l - min_l
        rot_range = range(rotations)
        if min_l != start_l:
            rot_range = reversed(rot_range)
        orbit = Orbit(
            [
                Wrap(
                    min_l + (max_diff / (rotations - 1) * i), 100.0, orbit_i + 1
                )
                for i in rot_range
            ],
            orbit_i + 1,
        )
        orbits.append(orbit)
        tl = [
            Wrap(min_l + (max_diff / (rotations - 1) * w))
            for w in range(rotations)
        ]
        if min_l == start_l and (orbit[0] != start_l):
            import pdb

            pdb.set_trace()
        if min_l == start_l and list(orbit) != sorted(tl):
            import pdb

            pdb.set_trace()
        if min_l != start_l:
            assert max_l == start_l
            assert min_l == end_l
            if not list(reversed(orbit)) == tl:
                import pdb

                pdb.set_trace()

        total += orbit.length()
    ply_len = total / parsed.ply

    print(
        ", ".join(
            f"orbit {orbit.orbit_num}, {len(orbit)} wraps, total length {orbit.length()}"
            for orbit in orbits
        )
    )
    plies: list[Ply] = [Ply()]
    if parsed.ply > 1:
        orbit_i = len(orbits) + 1
        orbit: Orbit = Orbit()
        while orbits:
            if not orbit:
                orbit = orbits.pop(-1)
                orbit_i -= 1
            while orbit:
                ply = plies[-1]
                wrap = orbit.pop(-1)
                ply.orbits.add(orbit_i)
                new_len = ply.length() + wrap

                # Todo figure out a tolerance
                if new_len >= ply_len:
                    partial_len = ply_len - ply.length()
                    tail, nose = wrap.split(partial_len)
                    ply.append(tail)
                    plies.append(Ply([nose]))
                    continue

                ply.append(wrap)
                if new_len == ply_len:
                    # move on to next ply with a complete wrap
                    plies.append(Ply())
                    continue

                if orbits and not orbit:
                    orbit = orbits.pop(-1)
                    orbit_i -= 1
    for ply_i, ply in enumerate(plies):
        print(f"{get_ordinal_suffix(ply_i+1)} ply ({ply.length()}):")
        wraps_by_orbit = ply.wraps_by_orbit()
        for orbit_i, orbit_wraps in reversed(wraps_by_orbit.items()):
            print()
            complete_wraps = [w for w in orbit_wraps if w.complete]
            if orbit_wraps[0].incomplete:
                print(f"Start with {orbit_wraps[0]} remainder")
            print(
                f"{len(complete_wraps)} wraps from orbit {orbit_i} {('with ' + str(ply[-1]) + ' tail') if ply[-1].incomplete else ''}."
            )

    print(
        f"total in: {total}({parsed.ply} ply: {ply_len})\ntotal ft: {total / 12} ply: {ply_len / 12})\n total yd: {total / 36} ply: {ply_len / 36})"
    )


if __name__ == "___main__":
    main()
