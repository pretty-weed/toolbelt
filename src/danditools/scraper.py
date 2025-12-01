import argparse
import os
from pathlib import Path
import re
import time
from typing import Collection, Iterator, Optional

import gdown
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

# Target web page URL (modify as needed)
DRIVE_URL_RE = re.compile("^(?:https?://)?drive.google.com")
DRIVE_URL_SUB_RE = re.compile(
    r"https?://drive\.google\.com/file/d/([0-9a-zA-Z_\-]+)/view(?:\?.*)"
)


def dir_path_type(value: str) -> Path:
    path = Path(value)
    if path.parent.is_dir() and not path.exists():
        path.mkdir()

    if not path.is_dir():
        raise ValueError(f"path {path} is not a path")
    return path


def is_google_drive(url: str) -> bool:
    return DRIVE_URL_RE.match(url) is not None


def get_drive_id(url: str) -> str:
    return DRIVE_URL_SUB_RE.match(url).group(1)


def xform_google_drive(url: str) -> str:

    return f"https://drive.google.com/uc?export=download&id={get_drive_id(url)}"


def main():
    """
    CLI main entry point
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target_regex", "--TR", action="append", type=re.compile
    )
    parser.add_argument(
        "--target_ext", "-T", action="append", dest="target_exts"
    )
    parser.add_argument("--follow", action="store_true")
    parser.add_argument("--out_dir", type=dir_path_type, default="scrape_out")
    parser.add_argument("start", nargs="+")

    parsed = parser.parse_args()
    print(parsed)
    for link_title, link in get_download_links(
        parsed.start,
        parsed.target_exts,
        parsed.target_regex,
        follow=parsed.follow,
    ):
        download_file(link, parsed.out_dir, link_title)


def get_download_links(
    start_pages: list[str],
    target_exts: Collection[str] | None = None,
    target_res: Collection[re.Pattern] | None = None,
    checked: set[str] | None = None,
    follow: bool | int = False,
) -> Iterator[str]:

    if not any([target_exts, target_res]):
        raise TypeError(
            "Either `target_exts` or `target_res` must be provided."
        )

    if target_exts is None:
        target_exts = ()
    else:
        target_exts = tuple(target_exts)
    if checked is None:
        checked = set().union(start_pages)

    for start_page in start_pages:
        response = requests.get(start_page)
        if response.status_code != 200:
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if follow and href.endswith((".htm", ".html", ".php", "/")):
                if follow is not True:
                    follow -= 1
                try:
                    yield from get_download_links(
                        href, checked=checked, follow=follow
                    )
                except HTTPError:
                    continue
            if not href.startswith("http"):
                import pdb

                pdb.set_trace()
            if href.endswith(target_exts) or any(
                tre.match(href) for tre in (target_res or [])
            ):

                # TODO not example dot com eh?
                full_url = (
                    href
                    if href.startswith("http")
                    else "https://example.com" + href
                )
                yield tag.text, full_url


def download_file(
    url, download_dir: Path, base_filename: str | None = None
):
    """Save the file from the link (append a number if the filename already exists)"""
    if base_filename is None:
        base_filename: str = url.split("/")[-1].rsplit("?", 1)[0]
    base_path: Path = Path(base_filename)  # type: ignore[arg-type]
    filepath: Path = download_dir.joinpath(base_path)
    counter = 1

    while filepath.exists():
        filepath = filepath.with_name(f"{base_filename}_{counter}").with_suffix(
            base_path.suffix
        )
        counter += 1
    if is_google_drive(url):
        url = xform_google_drive(url)
        print(f"Downloading: {url}")
        gdown.download(url, str(filepath))
        return
    print(f"Downloading: {url}")
    try:
        response = requests.get(url, stream=True, timeout=10)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved: {filepath}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

    time.sleep(
        1
    )  # Wait a bit to avoid sending too many requests in a short time
