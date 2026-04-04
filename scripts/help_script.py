from sys import argv
import scribus

for help_topic in argv[1:]:
    topic_val = getattr(scribus, help_topic)
    print(f"{help_topic}: {topic_val}")
    if callable(topic_val):
        help(topic_val)
