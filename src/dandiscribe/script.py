import argparse
import importlib

import dandiscribe

importlib.reload(dandiscribe)
import dandiscribe.util

importlib.reload(dandiscribe.util)
import dandiscribe.enums

importlib.reload(dandiscribe.enums)
import dandiscribe.calendar.main as dandi_cal

importlib.reload(dandi_cal)


def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--debug", action="store_true")
    dandi_cal.entry_point(
        routines_file="/home/dandelion/src/toolbelt/src/dandiscribe/routines.yml",
        debug=False,
    )


if __name__ == "__main__":
    main()
