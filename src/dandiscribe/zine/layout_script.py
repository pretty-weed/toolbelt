import sys


if "/usr/share/scribus/scripts" not in sys.path:
    sys.path.append("/usr/share/scribus/scripts")

import dandiscribe
import dandiscribe.enums
import dandiscribe.util
import dandiscribe.zine
from dandiscribe.zine import layout as zine_layout


zine_layout.create_from_current_doc(zine_layout.Layout.QUARTER)
