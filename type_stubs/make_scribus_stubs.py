# Keeping the path as not imported into this namespace for better clarity
import sys
from argparse import ArgumentParser, BooleanOptionalAction
from ast import AsyncFunctionDef, FunctionDef
from ast import parse as ast_parse
from ast import unparse as ast_unparse
from ast import walk as ast_walk
from collections.abc import Callable
from difflib import SequenceMatcher, unified_diff
from importlib import import_module
from importlib.machinery import FileFinder, SourceFileLoader
from inspect import (
    Signature,
    getmembers,
    isclass,
    ismemberdescriptor,
    ismodule,
    signature,
)
from os import linesep
from pathlib import Path
from sys import stderr
from types import MemberDescriptorType, ModuleType
from typing import Any, Self, get_type_hints

TEMP_FILE = Path().home().joinpath(".local", "tmp", "scribus_stubs.pyi")
STUBS_PATH = Path(__file__).parent

hint_map: dict[type[Any], str] = {
    int: "int",
    float: "float",
    str: "str",
    tuple: "tuple[]",
}


def import_stub_file(
    module_name: str, stubs_path: Path = STUBS_PATH
) -> ModuleType:

    tree = ast_parse(stubs_path.joinpath(f"{module_name}.pyi").read_text())
    for node in ast_walk(tree):
        if isinstance(node, (FunctionDef, AsyncFunctionDef)):
            print(f"Function: {node.name}")
            for arg in node.args.args:
                # ast.unparse converts the AST node back into a readable string
                hint = ast_unparse(arg.annotation) if arg.annotation else "None"
                # print(f"  Arg '{arg.arg}' type hint: {hint}")

            return_hint = ast_unparse(node.returns) if node.returns else "None"

    pyi_hook = FileFinder.path_hook((SourceFileLoader, [".pyi"]))
    sys.path_hooks.insert(0, pyi_hook)
    sys.path.insert(0, str(stubs_path.absolute()))

    try:
        # Clear cache and import the module dynamically
        sys.path_importer_cache.clear()
        return import_module(module_name)
    finally:
        # Clean up hooks to keep the environment pristine
        sys.path.pop(0)
        sys.path_hooks.pop(0)
        sys.path_importer_cache.clear()


def get_arg_str(element: Callable[..., Any], element_name: str) -> str:
    try:
        sig: Signature = signature(element)
    except Exception as exc:
        if "built-in function" not in str(exc):
            print(exc)
        return ""
    type_hints = get_type_hints(element, globals(), locals(), True)
    return ", ".join([f"{p}" for p in sig.parameters])


def function_formatter(
    element_name: str, element: Callable[..., Any], return_hint: str = ""
) -> str:
    return f"def {element_name}({get_arg_str(element, element_name)}){return_hint}: ..."


def class_formatter(
    element_name: str, element: Callable[..., Any], return_hint: None
) -> str:
    assert not return_hint
    print(dir(element))
    class_hint: str = (
        f"class {element_name}:\n    {function_formatter('__init__', element.__init__, ' -> None')}"
    )
    for member_name, member in getmembers(element):
        if callable(member):
            class_hint += f"\n    {function_formatter(member_name, member)}"
        elif ismemberdescriptor(member):
            class_hint += f"\n    {render_descriptor_hint(member_name, member)}"
        else:
            class_hint += (
                f"\n    {render_noncallable_hint(member_name, member)}"
            )
    return class_hint


def render_callable_hint(
    element_name: str,
    element: Callable[..., Any],
    previous: Callable[..., Any] | None = None,
):
    return_hint = ""
    suffix_comment = ""
    if isclass(element):
        formatter: Callable[..., str] = class_formatter
    else:
        # TODO
        suffix_comment = "TODO Need to fill in Return"
        return_hint = " -> ..."
        formatter: Callable[..., str] = function_formatter
        type_hints = get_type_hints(element)
        if "return" in type_hints:
            return_hint = type_hints["return"]
            suffix_comment = ""

        suffix_comment = "TODO need to fill in return"
    res = formatter(element_name, element, return_hint) + (
        f"  # {suffix_comment}" if suffix_comment else ""
    )

    if previous is not None:
        prev_return_hint = get_type_hints(previous).get("return")
        prev_res = formatter(element_name, previous, prev_return_hint)
        if prev_res != res:
            matcher = SequenceMatcher(
                None, prev_res.splitlines(), res.splitlines()
            )
            print("\n\n        ########### DIFF ###########           \n")
            diff = unified_diff(
                prev_res.splitlines(), res.splitlines(), "previous", "generated"
            )
            for line in diff:
                print(line)


def render_noncallable_hint(element_name: str, element: Callable[..., Any]):
    hint: str = hint_map.get(element.__class__, str(element.__class__))
    return f"{element_name}: {hint}"


def render_descriptor_hint(
    element_name: str, element: MemberDescriptorType
) -> str:
    return f"{element_name}: Any  # ToDo Find actual value, cannot compute"


class OtherTypes:
    @classmethod
    def getSpecific(cls, other: Any) -> type[Self]:
        class SpecificType(cls):
            my_type: str = str(other.__class__)

            def __str__(self):
                return self.my_type

        return SpecificType


def main() -> None:
    parser = ArgumentParser()
    _ = parser.add_argument("out_path")
    _ = parser.add_argument("--verbose", "-v", action="store_true")
    _ = parser.add_argument(
        "--check_previous",
        "--CP",
        action=BooleanOptionalAction,
        default=True,  # Set your preferred default state here
        help="Enable or disable comparison to previous file",
    )
    _ = parser.add_argument(
        "--interactive",
        action=BooleanOptionalAction,
        default=True,  # Set your preferred default state here
        help="Enable or disable interactive mode",
    )
    parsed = parser.parse_args()
    if parsed.check_previous:
        prev_hints = import_stub_file("scribus")
    else:
        prev_hints = None
    hints = {}
    outputters = []
    for el_name in dir(scribus):
        if prev_hints is not None and hasattr(prev_hints, el_name):
            prev_element = getattr(prev_hints, el_name)
        else:
            prev_element = None
        element = getattr(scribus, el_name)
        if callable(element):
            hint = render_callable_hint(el_name, element, prev_element)
        elif ismodule(element):
            continue
        else:
            hint = render_noncallable_hint(el_name, element)
        try:
            hints.setdefault(element.__class__, {})[element] = hint
        except TypeError:
            print(
                f"could not set hint for {el_name} by class: {element.__class__}"
            )
            key = OtherTypes.getSpecific(element)
            hints.setdefault(key, {})[key] = hint

    if parsed.out_path:
        out_file = Path(parsed.out_path).absolute()

        def outputter(content: str):
            with out_file.open("a") as fh:
                fh.write(content)
                if not content.endswith(linesep):
                    fh.write(linesep)

        outputters.append(outputter)
    if (not parsed.out_path) or (parsed.verbose):
        outputters.append(print)

    for outputter in outputters:
        print(f"outputting to {outputter}", file=stderr)
        for kind, kind_hints in hints.items():
            outputter(f"# =======\n# {kind}s\n# =======\n")
            for hint in kind_hints.values():
                outputter(hint)


if __name__ == "__main__":
    main()
