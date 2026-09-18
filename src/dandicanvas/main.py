from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup

from dandicanvas.scraper import Scraper

DISCUSSION_GET_SUFFIX = "/view?include_new_entries=1&include_enrollment_state=1"


class _NotSetStr(str):

    def __bool__(self) -> bool:
        return False


NotSetStr = _NotSetStr("Not Set")


@dataclass
class Organization:
    name: str
    courses: list[Course] = field(default_factory=lambda: list[Course]())

    def add_course(self, id: int, name: str = NotSetStr) -> Course:
        self.courses.append(Course(id, name))
        return self.courses[-1]


@dataclass
class Course:
    id: int
    name: str = field(default=NotSetStr)

    def scrape_conversations(self):
        pass


@dataclass
class Conf:
    orgs: list[Organization]
    courses: list[Course]


def scrape_conversation(
    org: str, course_id: int, conversation_id: int, outfile: Path | None = None
) -> BeautifulSoup:
    s: Scraper = Scraper()

    discusson_url = f"https://{org}.instructure.com/api/v1/courses/{course_id}/discussion_topics/{conversation_id}{DISCUSSION_GET_SUFFIX}"
    return s.scrape(discusson_url, outfile)


if __name__ == "__main__":
    # TOREMOVE for testing
    # IPDC round 1, Simpson Reading and Discussion 5
    print(
        scrape_conversation(
            "iliff", 3606465, 22697752, "ipdcv1_simpson_5_discuss.html"
        )
    )
