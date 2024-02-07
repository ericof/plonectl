from pathlib import Path

import pytest


@pytest.fixture
def relstorage_setings(settings_factory) -> Path:
    """Return relstorage settings."""
    path = settings_factory("relstorage.yaml")
    return path


@pytest.fixture(autouse=True)
def wrap_instance(tmp_workdir, relstorage_setings):
    return tmp_workdir
