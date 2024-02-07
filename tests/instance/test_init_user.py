from pathlib import Path
from plonectl.instance import init_user

import pytest


def test_create_init_user(instance_paths, settings):
    path = init_user.create_init_user(instance_paths, settings.instance)
    assert isinstance(path, Path)
    assert "admin:{SHA}" in path.read_text()


@pytest.mark.parametrize(
    "username,password",
    [
        ["admin", "admin"],
        ["root", "a very long password"],
    ],
)
def test__encode_user_info(username: str, password: str):
    result = init_user._encode_user_info(username, password)
    assert isinstance(result, str)
    assert result.startswith(f"{username}:{{SHA}}")
