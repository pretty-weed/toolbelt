import asyncio
from base64 import b64encode
from configparser import ConfigParser
from dataclasses import dataclass, field
from http.cookiejar import CookieJar
from itertools import chain
from json import dump
from pathlib import Path
from re import Pattern
from shutil import copy2
from typing import Any
from urllib.parse import urljoin

import browser_cookie3
from bs4 import BeautifulSoup, Tag
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from requests import RequestException, Response, get

LINUX_UA = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
)
LINUX_PLATFORM = "Linux x86_64"

HEADERS = {"User-Agent": LINUX_UA}

# TODO make configurable
FF_USE_SNAP = True

FF_DIR = (
    Path()
    .home()
    .joinpath(
        *(
            (["snap", "firefox", "common"] if FF_USE_SNAP else [])
            + [".mozilla", "firefox"]
        )
    )
)


def get_as_data_uri(asset_url: str) -> str | None:
    """Downloads an asset and converts it to a base64 Data URI."""
    try:
        res: Response = get(asset_url, headers=HEADERS, timeout=5)
    except RequestException as e:
        print(f"Failed to download asset {asset_url}: {e}")
    else:
        try:
            res.raise_for_status()
        except RequestException as e:
            print(f"Failed to download asset {asset_url} {e}")
        else:
            content_type: str = res.headers.get("Content-Type", "")
            b64_data: str = b64encode(res.content).decode("utf-8")
            return f"data:{content_type};base64,{b64_data}"

    return None


async def create_snapshot(url, output_file: Path | str | None) -> BeautifulSoup:
    """Navigates to a webpage using a spoofed context, inlines resources,

    and exports a single-file static HTML snapshot.
    """
    cookies: list[dict[str, Any]] = get_playwright_cookies(url)
    rendered_html: str = ""

    async with async_playwright() as p:
        browser: Browser = await p.firefox.launch(headless=True)

        context: BrowserContext = await browser.new_context(
            user_agent=LINUX_UA, viewport={"width": 1280, "height": 720}
        )

        # Override Javascript Fingerprints
        await context.add_init_script(
            f"""
            Object.defineProperty(navigator, 'platform', {{
                get: () => '{LINUX_PLATFORM}'
            }});
        """
        )

        if cookies:
            print(f"Injecting {len(cookies)} cookies...")
            for cookie in cookies:
                print(f"attempting to inject {cookie}")
                await context.add_cookies([cookie])

        page: Page = await context.new_page()
        print(f"Navigating to {url} as a Xubuntu Firefox client...")
        await page.goto(url, wait_until="networkidle")

        rendered_html = await page.content()
        await browser.close()

    # Parse and assemble single file structure
    soup: BeautifulSoup = BeautifulSoup(rendered_html, "html.parser")

    print("Inlining images...")
    img: Tag
    for img in soup.find_all("img"):
        src: str | list[str] | None = img.get("src")
        if src and not src.startswith("data:"):
            absolute_url: str = urljoin(url, src)
            data_uri: str | None = get_as_data_uri(absolute_url)
            if data_uri:
                img["src"] = data_uri

    print("Inlining stylesheets...")
    link: Tag
    for link in soup.find_all("link", rel="stylesheet"):
        href: str | None = link.get("href")
        if href:
            absolute_url = urljoin(url, href)
            try:
                css_res: Response = get(
                    absolute_url, headers=HEADERS, timeout=5
                )
                if css_res.status_code == 200:
                    style_tag: Tag = soup.new_tag("style")
                    style_tag.string = css_res.text
                    link.replace_with(style_tag)
            except Exception as e:
                print(f"Failed to embed CSS {absolute_url}: {e}")

    print("Stripping dynamic execution elements...")
    script: Tag
    for script in soup.find_all("script"):
        script.decompose()

    if output_file is not None:
        output_file = Path(output_file)
        with output_file.open("w", encoding="utf-8") as fh:
            fh.write(str(soup))

        print(f"Snapshot successfully saved to {output_file}")
    return soup


def get_ff_profile(profile_name: str | None = None) -> Path | None:
    config = ConfigParser()
    _ = config.read(str(FF_DIR.joinpath("profiles.ini")))
    selected: str | None = None
    for section in config.sections():
        if not section.startswith("Profile"):
            continue

        if config.get(section, "Name") == profile_name:
            return FF_DIR.joinpath(config.get(section, "Path"))

        if selected is None:
            # Get the first entry in case no default or match
            selected = section
            continue

        # Check if it is marked as the default profile
        if (
            config.has_option(section, "Default")
            and config.get(section, "Default") == "1"
        ):
            selected = section
            continue
    if selected is not None:
        return FF_DIR.joinpath(config.get(selected, "Path"))


def get_playwright_cookies(target_url) -> list[dict[str, str | int | None]]:
    """Loads cookies from  Firefox and formats them for Playwright."""
    print("Extracting cookies from local browser...")
    cookie_path = get_ff_profile().joinpath("cookies.sqlite")
    tmp_cookie_path = Path("/tmp").joinpath(
        cookie_path.parent.name, cookie_path.name
    )
    if not tmp_cookie_path.parent.exists():
        tmp_cookie_path.parent.mkdir(parents=True)
    copy2(cookie_path, tmp_cookie_path)

    domain = urljoin(target_url, "/")
    # import pdb
    # pdb.set_trace()
    cj_instructure: CookieJar = browser_cookie3.firefox(
        cookie_file=str(tmp_cookie_path), domain_name="instructure.com"
    )
    cj_google: CookieJar = browser_cookie3.firefox(
        cookie_file=str(tmp_cookie_path), domain_name="google.com"
    )

    playwright_cookies: list[dict[str, str | int | None]] = []
    for cookie in chain(cj_instructure, cj_google):
        cookie_dict: dict[str, str | int | None] = {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
        }
        if cookie.expires:
            cookie_dict["expires"] = cookie.expires // 1000
        else:
            cookie_dict["expires"] = -1
        playwright_cookies.append(cookie_dict)

    # TOREMOVE
    with Path("playwright_cookies.json").open("w") as fh:
        print(f"playwright cookies: {playwright_cookies}")
        dump(playwright_cookies, fh)
    return playwright_cookies


@dataclass
class LinkHandler:
    scraper: Scraper
    url_matcher: Pattern[str] | None = None
    query_selector: str | None = None


@dataclass
class Scraper:
    url_matcher: Pattern[str] | None = None
    link_handlers: list[LinkHandler] = field(
        default_factory=lambda: list[LinkHandler]()
    )

    def scrape(
        self, url: str, outfile: str | Path | None = None
    ) -> BeautifulSoup:
        result: BeautifulSoup = asyncio.run(
            create_snapshot(url=url, output_file=outfile)
        )

        return result
