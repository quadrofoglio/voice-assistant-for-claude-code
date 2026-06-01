import sys
import pathlib


def bundle_dir() -> pathlib.Path:
    """Directory containing bundled read-only data (config, assets, hook).
    Points to _internal/ when frozen, project root when running from source."""
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys._MEIPASS)
    return pathlib.Path(".")


def exe_dir() -> pathlib.Path:
    """Directory next to the exe — for runtime data the user may add/replace
    (voices, piper_bin). Falls back to project root when running from source."""
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys.executable).parent
    return pathlib.Path(".")
