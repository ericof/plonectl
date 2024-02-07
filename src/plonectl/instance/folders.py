from pathlib import Path
from plonectl import types


INSTANCE_SUBFOLDERS = (
    "target",
    "location_clienthome",
    "location_log",
    "db_blobs_location",
    "environment/CHAMELEON_CACHE",
    "db_filestorage_location",
)

INSTANCE_CONFIG_PATH = "etc"


def _get_str_value(base_key: str, settings: types.InstanceSettings) -> str:
    """Traverse settings to get a str value."""
    keys = base_key.split("/")
    value = settings
    while keys:
        key = keys.pop(0)
        default = {} if keys else ""
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            value = getattr(value, key, default)
    return value if isinstance(value, str) else ""


def _get_or_create_folder(value: types.StrPath) -> Path:
    """Create new folder if it does not exist."""
    path = Path(value).resolve()
    if not path.exists():
        path.mkdir(parents=True)
    return path


def prepare_instance_folders(settings: types.InstanceSettings) -> types.InstancePaths:
    """Prepare instance folders."""
    from .init_user import create_init_user

    folders = {}
    for key_path in INSTANCE_SUBFOLDERS:
        value = _get_str_value(key_path, settings)
        if not value:
            continue
        if key_path == "db_filestorage_location":
            # This points to a file, so we return the parent
            value = "/".join(value.split("/")[:-1])
        path = _get_or_create_folder(value)
        folders[key_path] = path

    config_path = _get_or_create_folder(folders["target"] / INSTANCE_CONFIG_PATH)

    instance_paths = types.InstancePaths(
        folders["target"],
        folders["location_clienthome"],
        config_path,
    )
    # Init User
    create_init_user(instance_paths, settings)
    return instance_paths
