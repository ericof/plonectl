from plonectl import cli
from plonectl import types
from typer import Typer
from typer.testing import CliRunner

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


@pytest.fixture
def runner(instance_paths) -> CliRunner:
    runner = CliRunner()
    yield runner


@pytest.fixture
def cli_app() -> Typer:
    return cli.cli
