import sys

if "/usr/share/scribus/scripts" not in sys.path:
    sys.path.append("/usr/share/scribus/scripts")

import importlib
import dandiscribe

importlib.reload(dandiscribe)
import dandiscribe.util

importlib.reload(dandiscribe.util)
import dandiscribe.enums

importlib.reload(dandiscribe.enums)
import dandiscribe.calendar

importlib.reload(dandiscribe.calendar)
import dandiscribe.calendar.main

importlib.reload(dandiscribe.calendar.main)

dandiscribe.calendar.main.entry_point(
    routines_file="/home/dandelion/src/toolbelt/src/dandiscribe/routines.yml",
    debug=False,
)
