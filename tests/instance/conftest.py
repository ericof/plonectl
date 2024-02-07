from plonectl import types

import pytest


@pytest.fixture(autouse=True)
def wrap_instance(tmp_workdir, default_settings):
    return tmp_workdir


@pytest.fixture
def settings(wrap_instance):
    from plonectl.settings import get_settings

    settings = get_settings(wrap_instance)
    return settings


@pytest.fixture
def instance_paths(settings) -> types.InstancePaths:
    from plonectl.instance.folders import prepare_instance_folders

    return prepare_instance_folders(settings.instance)
