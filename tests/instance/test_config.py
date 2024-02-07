from pathlib import Path
from plonectl import types
from plonectl.instance import config

import pytest


@pytest.mark.parametrize(
    "attr",
    [
        "zcmlconf",
        "wsgiconf",
        "zopeconf",
    ],
)
def test_generate_config_files(instance_paths, settings, attr: str):
    result = config.generate_config_files(instance_paths, settings)
    assert isinstance(result, types.InstanceConfigFiles)
    path = getattr(result, attr)
    assert isinstance(path, Path)
    assert path.exists() is True
    assert path.is_file() is True
