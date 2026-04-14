import re
from sys import argv
from typing import Any
import scribus

NAME_REGEX = re.compile(r"^[A-Za-z_]\w*$")

for help_topic in argv[1:]:
    topic_vals: dict[str, Any]
    if NAME_REGEX.match(help_topic):
        topic_vals = {help_topic: getattr(scribus, help_topic)}
    else:
        topic_re = re.compile(help_topic)
        topic_vals = dict(
            (n, getattr(scribus, n)) for n in dir(scribus) if topic_re.match(n)
        )
    for topic, topic_val in topic_vals.items():
        print(f"{topic} = {repr(topic_val)}")
        if callable(topic_val):
            help(topic_val)
