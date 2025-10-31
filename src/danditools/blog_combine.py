from argparse import ArgumentParser
from copy import copy
from functools import cache, partial
import re
from typing import Any, Callable
from bs4 import BeautifulSoup
from pathlib import Path, PurePath

def existing_path(in_val: str="."):
        res = Path(in_val)
        if not res.exists():
            raise ValueError("%s does not exist", in_val)
        return res

# should any be str?
def filter_for_attr_val(element, attr: str, value: Any) -> bool:
    return element.attrs.get(attr) == value
    

def filter_for_data_hook_value(element, value:str) -> bool:
    return element.attrs.get("data-hook") == value

def merge_rcv_block_divs(div1, div2):
    """
    Merge the children of div2 into div1 correctly
    """
    for child in div2.children:
        # maybe only recieve blocks check into this
        div1.append(copy(child))
        assert list(div1.children)[-1] == child
        assert list(div1.children)[-1].parent == div1

class IncorrectAssumptionError(Exception):
    """what it says on the tin"""

def get_reciever_div(soup):
    first = soup.findChildren(partial(filter_for_attr_val, attr="data-hook", value="rcv-block-first"))
    last = soup.findChildren(partial(filter_for_attr_val, attr="data-hook", value="rcv-block-last"))
    assert len(last) == 1 and len(first) == 1
    last = last[0]
    first = first[0]
    assert not list(last.children) or list(first.children)
    reciever_div = None
    for child in first.next_siblings:
        if child.attrs.get("data-hook") == "rcv-block-last":
            break
        if reciever_div is not None:
            raise IncorrectAssumptionError("I thought that there would be one of these")
        reciever_div = child
    if reciever_div is None:
        raise IncorrectAssumptionError("I thought there would be one of these")
    return reciever_div



def main():
    parser = ArgumentParser()
    parser.add_argument("to_combine", type=existing_path, nargs="+")
    parser.add_argument("target", type=Path)
    parsed = parser.parse_args()
    print(parsed)
    soup = None
    reciever_div = None
    while parsed.to_combine:
        if soup is None:
            soup = BeautifulSoup(parsed.to_combine.pop(0).read_text(), features="html.parser")
            reciever_div = get_reciever_div(soup)
        this = parsed.to_combine.pop(0)
        this_soup = BeautifulSoup(this.read_text(), features="html.parser")
        this_reciever = get_reciever_div(this_soup)
        for child in this_reciever.children:
            # rmeove extra footers eh?
            if child.name in  ("footer", "header"):
                continue
            to_remove = []
            for element in child.descendants:
                nm = element.name
                if "BEN" in str(element.text).upper() and "cher" not in element.text.lower(): # element.name not in (None, "em", "svg", "strong", "blockquote", "figure", "path", "p", "wow-image", "a", "u", "div", "span", "br", "button", "img"):
                    import pdb
                    pdb.set_trace()
                #to_remove.append(element)
            for element in to_remove:
                element.extract()
            child.extract()
            print(f"appending <{child.name} {child.attrs}>")
            reciever_div.append(child)
        
        parsed.target.write_text(str(soup))

    to_extract = []
    def checker(element):
        res = element.attrs.get("data-hook") in ("post-footer", "recent-posts")
        if not res and ("recent" in str(element).lower() or "views" in str(element).lower()):
            import pdb
            pdb.set_trace()
    # ToDo maybe: leave recent posts at end
    for rp in soup.find_all(lambda ch: ch.attrs.get("data-hook") in ("post-footer", "recent-posts")):
        to_extract.append(rp)
    for rp in to_extract:
        rp.extract()

    parsed.target.write_text(str(soup))

if __name__ == "__main__":
    main()