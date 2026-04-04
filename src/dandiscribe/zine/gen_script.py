import sys


if "/usr/share/scribus/scripts" not in sys.path:
    sys.path.append("/usr/share/scribus/scripts")

import dandiscribe
import dandiscribe.enums
from dandiscribe.layout import PAPER_LETTER
import dandiscribe.util
import dandiscribe.zine
from dandiscribe.zine import layout as zine_layout


zine_layout.generate_pages(16, 4, print_size=PAPER_LETTER)
