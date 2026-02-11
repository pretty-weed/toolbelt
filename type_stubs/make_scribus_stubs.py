from typing import Any, Callable

from inspect import Signature, getmembers, isclass, ismemberdescriptor, ismodule, signature
import json

hint_map = {
	int: "int",
	float: "float",
	str: "str",
	tuple: "tuple[]",
}

def get_arg_str(element: Callable[..., Any], element_name: str) -> str:
  try:
    sig: Signature = signature(element)
  except Exception as exc:
    if "built-in function" not in str(exc):
      print(exc)
    return ""
  return ", ".join([str(p) for p in sig.parameters])


def function_formatter(element_name: str, element: Callable[..., Any], return_hint: str = "") -> str:
  return f"def {element_name}({get_arg_str(element, element_name)}){return_hint}: ..."


def class_formatter(element_name: str, element: Callable[..., Any], return_hint: None) -> str:
  assert not return_hint
  print(dir(element))
  class_hint: str = f"class {element_name}:\n    {function_formatter('__init__', element.__init__, ' -> None')}"
  for member_name, member in getmembers(element):
    if callable(member):
      class_hint += f"\n    {function_formatter(member_name, member)}"
    elif ismemberdescriptor(member):
      class_hint += f"\n    {}"
    else:
      class_hint += f"\n    {render_noncallable_hint(member_name, member)}"
  return class_hint

def render_callable_hint(element_name: str, element: Callable[..., Any]):
  return_hint = ""
  suffix_comment = ""
  if isclass(element):
    formatter: Callable[..., str] = class_formatter
  else:
    # TODO 
    return_hint = " -> ..."
    formatter: Callable[..., str] = function_formatter
    suffix_comment = "TODO need to fill in return"
  return formatter(element_name, element, return_hint) + (f"  # {suffix_comment}" if suffix_comment else "")


def render_noncallable_hint(element_name: str, element: Callable[..., Any]):
  hint: str = hint_map.get(element.__class__, str(element.__class__))
  return f"{element_name}: {hint}"


def main() -> None:
  hints = {}
  for el_name in dir(scribus):
    element = getattr(scribus, el_name)
    if callable(element):
      hint = render_callable_hint(el_name, element)
    elif ismodule(element):
      continue
    else:
      hint = render_noncallable_hint(el_name, element)
    try:
      hints.setdefault(element.__class__, {})[element]=hint
    except TypeError:
      print(f"could not save hint for {el_name}")
    
  for kind, kind_hints in hints.items():
    print(f"# =======\n# {kind}s\n# =======\n")
    for hint in kind_hints.values():
      print(hint)

main()
