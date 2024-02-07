from pathlib import Path
from plonectl import types


def get_settings(cwd: Path) -> types.LoadedSettings:
    """Load settings from configuration files, environment vars."""
    from .loader import _load_settings

    keys = ("instance", "plonectl")
    raw_settings = _load_settings(root_path=cwd)
    filtered = {k: v for k, v in raw_settings.items() if k in keys}
    settings = types.LoadedSettings(**filtered)
    return settings
