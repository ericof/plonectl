from pathlib import Path

import pytest


@pytest.fixture
def default_settings(settings_factory) -> Path:
    """Return the initial_user configuration."""
    path = settings_factory("initial_user.yaml")
    return path
