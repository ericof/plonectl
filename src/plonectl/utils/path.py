from pathlib import Path
from plonectl import types


def relative_path(path: types.StrPath, base_path: types.StrPath = None) -> Path:
    """Return relative path."""
    base_path = (Path(base_path) if base_path else Path().cwd()).resolve()
    path = Path(path)
    try:
        return path.relative_to(base_path)
    except ValueError:
        # Not relative path, return the full path
        return path
