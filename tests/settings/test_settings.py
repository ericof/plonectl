from pathlib import Path
from plonectl import settings
from plonectl import types
from typing import Callable

import pytest


@pytest.mark.parametrize(
    "name",
    [
        "default",
        "ctl_debug",
        "data_directory",
        "initial_user",
    ],
)
def test_get_settings_response(
    tmp_workdir: Path,
    settings_factory: Callable,
    name: str,
):
    # Create settings file
    settings_factory(f"{name}.yaml")
    result = settings.get_settings(tmp_workdir)
    assert isinstance(result, types.LoadedSettings)
    assert isinstance(result.plonectl, types.PloneCTLSettings)
    assert isinstance(result.instance, types.InstanceSettings)
