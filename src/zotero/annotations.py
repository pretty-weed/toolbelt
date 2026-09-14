"""
dandy_lib.zotero.annotations
"""

import sys
from argparse import ArgumentParser
from dataclasses import dataclass, field
from pathlib import Path, PosixPath, PurePath, WindowsPath
from typing import Any, Self

from pylatex import Document, Package, Section, Subsection
from pylatex.base_classes import Environment
from pylatex.basic import NewLine
from pylatex.utils import NoEscape, bold, italic
from pyzotero import Zotero
from pyzotero.errors import UnsupportedParamsError
from yaml import SafeDumper, SafeLoader, safe_dump, safe_load
from yaml.nodes import ScalarNode

CONF_FILENAME = "zotero-annotations.yaml"
# Todo make this more general less hacky
DEFAULT_CONF_DIR = Path.home().joinpath(".config")
DEFAULT_CONF_FILE = DEFAULT_CONF_DIR.joinpath(CONF_FILENAME)

API_KEY_KEY = "apiKey"
API_KEY_ = "api"
LIBRARY_ID_KEY = "libraryID"


class TColorBox(Environment):
    _latex_name = "tcolorbox"
    packages = [Package("tcolorbox")]


class Zot(Zotero):
    _item_cache: dict[str, dict[str, Any]] = {}

    def get_item_annotations(
        self, itemKey=None, limit=100, **kwargs
    ) -> list[dict[str, Any]]:
        res: list[dict[str, Any]] = []
        query_limit = 100
        start = 0
        if limit < 0:
            limit = float("inf")
        query_res = self.item(itemKey, limit=query_limit, start=start, **kwargs)
        if query_res["data"]["itemType"] == "annotation":
            res.append(query_res)
        try:
            children = self.children(itemKey)
        except UnsupportedParamsError:
            pass
        else:
            for child in children:
                if child["data"]["itemType"] == "annotation":
                    res.append(child)
                else:
                    res.extend(self.get_item_annotations(child["key"]))

        return res

    def item(self, itemID, **kwargs) -> dict[str, Any]:
        if itemID in self._item_cache:
            return self._item_cache[itemID]
        res = super().item(itemID, **kwargs)
        self._item_cache[itemID] = res
        return res

    def top_item(self, item_id: str) -> dict[str, Any]:
        item = self.item(item_id)
        while item["data"].get("parentItem"):
            item = self.item(item["data"]["parentItem"])
        return item

    def get_attachment_annotations(
        self, attachment: dict[str:Any]
    ) -> list[dict[str:Any]]:

        return [
            child
            for child in self.children(attachment["key"])
            if child["data"]["itemType"] == "annotation"
        ]


# Yaml loaders
def path_representer(dumper: SafeDumper, data) -> ScalarNode:
    # This saves the path wrapped in a custom label: !path "your/path/here"
    return dumper.represent_scalar("!path", str(data))


# 2. DEFINE HOW TO LOAD (CONSTRUCT) A PATH
def path_constructor(loader: SafeLoader, node: ScalarNode):
    # This converts the tagged text back into a real Path object
    value = loader.construct_scalar(node)
    return Path(value)


for path_type in [PurePath, Path, PosixPath, WindowsPath]:
    SafeDumper.add_representer(path_type, path_representer)
SafeLoader.add_constructor("!path", path_constructor)


@dataclass
class Conf:
    conf_path: Path = DEFAULT_CONF_FILE

    api_key: tuple[Path | str, Path | str | None] | None = None
    library_id: str | None = None
    conf: dict[str, str | Path] | None = field(default=None, init=False)

    @classmethod
    def new_load(cls, conf_path: None | Path = None) -> Self:
        path = conf_path if conf_path is not None else DEFAULT_CONF_FILE
        cnf = cls(path)
        cnf.load(path)

        return cnf

    def dump(self, conf_path: Path | None = None) -> None:
        conf_path = conf_path if conf_path is not None else self.conf_path
        conf = dict(self.conf) if self.conf is not None else {}
        if self.library_id is not None:
            conf[LIBRARY_ID_KEY] = self.library_id
        with conf_path.open("w") as fh:
            safe_dump(conf, fh)

    def load(self, conf_path: Path | None = None):
        if conf_path is not None and conf_path != self.conf_path:
            # todo better logging
            print(f"Changing conf path from {self.conf_path} to {conf_path}")
            self.conf_path = conf_path
        if self.conf_path.is_file():
            with self.conf_path.open() as fh:
                self.conf = safe_load(fh)
        else:
            raise ValueError(f"Conf file {self.conf_path} does not exist")

        if self.conf is not None and LIBRARY_ID_KEY in self.conf:
            self.library_id = self.conf[LIBRARY_ID_KEY]

    def get_key(self) -> str | None:
        if self.api_key is not None:
            raw: Path | str = self.api_key[0]
            if self.api_key[1] is not None:
                raw = self.api_key[1]
        else:
            if self.conf is None:
                self.load()
                if self.conf is None:
                    return None

            raw: None | Path | str = self.conf.get(API_KEY_KEY)

        match raw:
            case str():
                self.api_key = (raw, raw)
                return raw
            case None:
                raise AttributeError("No Key available")
            case _:
                # assume Path()
                unraw = raw.read_text()
                self.api_key = (raw, unraw)
                return unraw


def _check_extra():
    try:
        from pyzotero import Zotero
    except ImportError:
        print("Please install danditools[zotero]' to use this command.")
        sys.exit(13)


def make_latex(
    items: dict[str, tuple[dict[str, Any], list[dict[str, Any]]]],
) -> str:

    doc = Document()
    doc.packages.append(Package("tcolorbox", "most"))
    doc.packages.append(Package("xcolor", "dvipsnames"))
    doc.append(Section("Zotero Annotations"))
    for top_id, top_item_and_annots in items.items():
        top_item, annots = top_item_and_annots
        doc.append(Subsection(top_item["data"]["title"]))
        # todo find double wrapped list
        for aa in annots:
            for annot in aa:
                # Arguments: \begin{tcolorbox}[options], Title, Body text
                with doc.create(
                    TColorBox(
                        options=NoEscape(
                            ", ".join(
                                [
                                    "enhanced",
                                    "skin=bicolor",
                                    "colback=RoyalPurple!10",
                                    "colbacklower=RoyalPurple!2",
                                    "colframe=Goldenrod!60!black",
                                    "arc=1mm",
                                ]
                            ),
                        )
                    )
                ):
                    if "annotationText" in annot["data"]:
                        doc.append(annot["data"]["annotationText"])
                    doc.append(
                        italic(f"({annot['data']['annotationPageLabel']})")
                    )
                    comment = annot["data"].get("annotationComment")
                    if comment:
                        doc.append(NoEscape(r"\tcblower"))
                        doc.append(bold("Comment: "))
                        doc.append(comment)
                        doc.append(NewLine())

    return doc.dumps()


def get():
    _check_extra()

    parser = ArgumentParser()
    _ = parser.add_argument("--config", "-c", default=DEFAULT_CONF_FILE)
    parsed, _ = parser.parse_known_args()
    config = Conf.new_load(parsed.config)
    _ = parser.add_argument(
        "--library_id", "--li", "-l", default=config.library_id
    )
    _ = parser.add_argument("--local", "-L", action="store_true")
    _ = parser.add_argument("--query", "-q", action="append")
    _ = parser.add_argument("--item", "-i", action="append")
    _ = parser.add_argument("--count", "-C", type=int, default=100)
    _ = parser.add_argument("--quiet", "-Q", action="store_true")
    _ = parser.add_argument(
        "--output", "-o", choices=["yaml", "latex"], default="yaml"
    )
    _ = parser.add_argument("--outfile", "-O")
    parsed = parser.parse_args()

    if parsed.local:
        zot = Zot("0", "user", local=True)
    else:
        zot = Zot(parsed.library_id, "user", config.get_key())
    res = []
    items = list(parsed.item or [])
    queries = list(parsed.query or [])
    for item in items:
        q_res = zot.item(item)
        if q_res:
            res.extend(zot.get_item_annotations(q_res["data"]["key"]))

    q_starts = dict[str, int]((q, 0) for q in queries)
    while queries and len(res) < parsed.count:
        for query in list(queries):

            q_res: list[dict[str, Any]] = zot.items(
                q=query, start=q_starts[query]
            )
            q_starts[query] += len(q_res)

            if not q_res:
                queries.remove(query)

            for r in q_res:
                annots = zot.get_item_annotations(r["key"])
                res.extend(annots)
    collected_res: dict[str, tuple[dict[str, Any], list[dict[str, Any]]]] = {}
    for r in res:
        parent = zot.top_item(r["key"])

        collected_res.setdefault(parent["key"], (parent, []))[1].append(res)
    # Get top items
    to_output = ""
    match parsed.output:
        case "yaml":
            to_output = safe_dump(collected_res)
        case "latex":
            to_output = make_latex(collected_res)
    if parsed.outfile:
        Path(parsed.outfile).write_text(to_output)
    if not parsed.quiet:
        print(f"found {len(res)} items")
        print(to_output)


get()
