import importlib

import dandiscribe

importlib.reload(dandiscribe)
import dandiscribe.util

importlib.reload(dandiscribe.util)
import dandiscribe.enums

importlib.reload(dandiscribe.enums)
import dandiscribe.calendar

importlib.reload(dandiscribe.calendar)

dandiscribe.calendar.main.entry_point(
    routines_file="/home/dandelion/src/toolbelt/src/dandiscribe/routines.yml",
    debug=False,
)
