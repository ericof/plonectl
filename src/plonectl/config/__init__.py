from pathlib import Path


def instance_folder(path: str) -> Path:
    """Instance folder."""
    folder = Path(path).resolve()
    return folder


def config_path(instance: Path, path: str) -> Path:
    """Configuration path."""
    config = instance / path
    if not config.exists():
        raise ValueError(f"No configuration available at {config}")
    return config
