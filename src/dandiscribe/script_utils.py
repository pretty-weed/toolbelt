import importlib
import sys

def reload() -> None:
    for name, mod in dict(sys.modules.items()).items():
        if name == "__name__":
            print(f"skipping reload of {name}")
            continue
        if name.startswith(("dandiscribe", "danditools", "dandy_lib")):
            
            importlib.reload(mod)