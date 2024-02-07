from pathlib import Path
from plonectl import types

import pytest


@pytest.fixture
def tmp_workdir(workdir_factory) -> Path:
    return workdir_factory()


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


@pytest.fixture
def instance_config(settings, instance_paths) -> types.InstanceConfigFiles:
    from plonectl.instance import generate_config_files

    return generate_config_files(instance_paths, settings)
