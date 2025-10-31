"""
This might be a one trick pony, but the transcripts for the saint albans
had this strange artifact
"""

from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path, PurePath

Line = namedtuple("Line", ["speaker", "timestamp", "line"])

def main():
    parser = ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parsed = parser.parse_args()
    
    for file in parsed.files:
        out_lines = []
        prefix = 0
        suffix = 0
        timestamp = speaker = line_text = None
        last_line = None
        for in_line in file.read_text().splitlines():
            in_line = in_line.strip()
            if not in_line or in_line == last_line:
                continue
            last_line = in_line
            if out_lines and out_lines[-1].line.strip() == in_line:
                continue
            elif len(in_line.split(":")) == 2 and all(side.isdigit() for side in in_line.split(":")):
                if timestamp is not None:
                    out_lines.append(Line(speaker, timestamp, in_line))
                timestamp = in_line
                speaker = line_text = None
            elif timestamp is not None and speaker is None:
                speaker = in_line
            elif line_text:
                line_text = "\n\n".join([line_text, in_line])
            else:
                line_text = in_line

        for out_line in out_lines:
            print(out_line)
            print(out_line.line)
            
