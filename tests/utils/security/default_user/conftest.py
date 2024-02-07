from pathlib import Path

import pytest


@pytest.fixture
def default_settings(settings_factory) -> Path:
    """Return the default configuration."""
    path = settings_factory("default.yaml")
    return path
