import argparse
from collections import namedtuple
import dataclasses
import json
from logging import getLogger, INFO, DEBUG
import re
import subprocess
import typing

import yaml

logger = getLogger(__name__)

SCREEN_RE = re.compile(rb"(?:^|\n)Screen (?P<id>\d+): minimum (?P<min_x>\d+) ?x ?(?P<min_y>\d+), current (?P<cur_x>\d+) ?x ?(?P<cur_y>\d+), maximum (?P<max_x>\d+) ?x ?(?P<max_y>\d+)(?P<displays>(?:\n(?!Screen \d).*)*)")
DISP_RE = re.compile(rb"\n(?P<id>[a-zA-Z0-9\-]+) (?P<conn>(?:dis)?connected) (?P<primary>primary )?(?P<conf>\d+x\d+(?:\+\d+\+\d+ )?(?:left )?)?\((?P<stuff>(?:[a-z]+\s*)*)\)(?P<real_size> \d+[a-z]+ x \d+[a-z]+)?(?P<modes>(?:\n\s.*)*)")
MODE_RE = re.compile
"""
Screen 0: minimum 320 x 200, current 5040 x 3840, maximum 16384 x 16384
eDP connected primary 2880x1800+2160+2040 (normal left inverted right x axis y axis) 302mm x 188mm
   2880x1800    120.00*+  60.00  
   1920x1200    120.00  
   1920x1080    120.00  
   1600x1200    120.00  
   1680x1050    120.00  
   1280x1024    120.00  
   1440x900     120.00  
   1280x800     120.00  
   1280x720     120.00  
   1024x768     120.00  
   800x600      120.00  
   640x480      120.00  
HDMI-A-0 disconnected (normal left inverted right x axis y axis)
DisplayPort-0 disconnected (normal left inverted right x axis y axis)
DisplayPort-1 disconnected (normal left inverted right x axis y axis)
DisplayPort-2 disconnected (normal left inverted right x axis y axis)
DisplayPort-3 disconnected (normal left inverted right x axis y axis)
DisplayPort-4 disconnected (normal left inverted right x axis y axis)
DisplayPort-5 disconnected (normal left inverted right x axis y axis)
DisplayPort-6 disconnected 2160x3840+0+0 left (normal left inverted right x axis y axis) 0mm x 0mm
DisplayPort-7 disconnected (normal left inverted right x axis y axis)
DisplayPort-8 disconnected (normal left inverted right x axis y axis)
  3840x2160 (0x6b) 297.000MHz +HSync +VSync
        h: width  3840 start 4016 end 4104 total 4400 skew    0 clock  67.50KHz
        v: height 2160 start 2168 end 2178 total 2250           clock  30.00Hz

"""

Dims = namedtuple("Dims", ["x", "y"])
_Rate = namedtuple("Rate", ["rate", "active", "preferred"])

class Rate(_Rate):
    def __init__(self, rate: float, active: bool = False, preferred: bool = False):
        return super().__init__(rate, active, preferred)

@dataclasses.dataclass
class Mode:
    dims: Dims
    refresh_rates: list[Rate]

    PREFIX_RE: typing.ClassVar = re.compile(rb"^\s+(?=\d)", re.MULTILINE)
    MODE_RE: typing.ClassVar = re.compile(rb"^ *(\d+)x(\d+)(\s+.*)$")
    REFRESH_RE: typing.ClassVar = re.compile(rb"(\d+(?:\.\d+)?)(?:MHz)?\*?\+?")

    @classmethod
    def parse(cls, in_str: str) -> "Mode":
        mode_match = cls.MODE_RE.match(in_str.lstrip(b"\n"))
        assert mode_match is not None
        x, y, refresh = mode_match.groups()
        refresh_rates = [dir(m) for m in cls.REFRESH_RE.finditer(in_str[mode_match.endpos:].lstrip(b"\n"))]
        return cls(Dims(x, y), refresh_rates)

    @classmethod
    def parse_many(cls, in_str: str) -> typing.Iterator["Mode"]:
        
        prefix_lens = set(len(m.group()) for m in cls.PREFIX_RE.finditer(in_str))

        if not prefix_lens:
            return
        prefix_len = min(prefix_lens)
        for mode_str in re.finditer(r"^\s+(\d+)x(\d+)\s+(\d+\.\d+)".encode(), in_str, re.MULTILINE):
            
            yield(cls.parse(mode_str.group()))


@dataclasses.dataclass
class Display:
    name: str
    connected: bool
    primary: bool = False
    active_conf: str = None
    stuff: str = None
    size: tuple[int, int] = None
    modes: list[Mode] = dataclasses.field(default_factory=list)

def query(verbose: bool = False):
    cmd = [
        "xrandr", "--query"
    ]
    if verbose:
        cmd.append("--verbose")
    return subprocess.check_output(cmd)

def parse(verbose: bool = False):

    raw = query(verbose=verbose)
    records = {}
    screen_record = None

    screen_res = SCREEN_RE.finditer(raw)
    for screen in screen_res:
        disps = screen.groupdict()["displays"]

        for disp_res in DISP_RE.finditer(disps):
            gd = disp_res.groupdict()
            display = Display(
                gd["id"], 
                connected=gd["conn"].strip() == b"connected", 
                primary=bool(gd["primary"]), 
                modes=list(Mode.parse_many(gd["modes"])),
                stuff=gd.get("stuff"),
            )
            print(disp_res.groupdict())
            print(display)
        
    """
    for line in raw.splitlines():
        if not line.strip(): 
            continue
        if line.startsWith("Screen "):
            screen_record = []
            records[]
        elif line == line.lstrip():
            # No whitespace, it's a new monitor


        else:
            # has whitespace at beginning, continuation of previous record
            if not screen_record:
                raise ValueError("did not understand query out")
            

    """



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output", "-o", choices=["yaml", "json"])

    parsed = parser.parse_args()

    parse(verbose=parsed.verbose)

    