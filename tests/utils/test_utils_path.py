from pathlib import Path
from plonectl.utils import path

import pytest


@pytest.mark.parametrize(
    "path_,base_path,expected",
    [
        ["{tmp_workdir}/instance", "{tmp_workdir}", "instance"],
        ["{tmp_workdir}/instance", "", "instance"],
        ["/data", "{tmp_workdir}", "/data"],
        ["/data", "", "/data"],
        ["{tmp_workdir}/foo.yaml", "{tmp_workdir}", "foo.yaml"],
        ["{tmp_workdir}/foo.yaml", "", "foo.yaml"],
    ],
)
def test_relative_path(expand_path, path_: str, base_path: str, expected: str):
    path_ = expand_path(path_)
    base_path = expand_path(base_path)
    expected = Path(expand_path(expected))
    result = path.relative_path(path_, base_path)
    assert result == expected
