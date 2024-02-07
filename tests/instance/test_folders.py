from pathlib import Path
from plonectl import types
from plonectl.instance import folders

import pytest


@pytest.mark.parametrize(
    "raw_path,exists,is_dir",
    [
        ["{tmp_workdir}/instance/var", True, True],
        ["{tmp_workdir}/instance/var/filestorage", True, True],
        ["{tmp_workdir}/instance/var/blobs", True, True],
        ["{tmp_workdir}/instance/etc", True, True],
        ["{tmp_workdir}/instance/inituser", True, False],
    ],
)
def test_prepare_instance_folders(
    settings, expand_path, raw_path: str, exists: bool, is_dir: bool
):
    path = Path(expand_path(raw_path))
    result = folders.prepare_instance_folders(settings.instance)
    assert isinstance(result, types.InstancePaths)
    assert path.exists() is exists
    assert path.is_dir() is is_dir


@pytest.mark.parametrize(
    "value",
    [
        "foo",
        "bar",
        "1234",
    ],
)
def test__get_or_create_folder(tmp_workdir, value: str):
    path = f"{tmp_workdir}/{value}"
    folder = folders._get_or_create_folder(path)
    assert isinstance(folder, Path)


@pytest.mark.parametrize(
    "value",
    [
        "foo",
        "bar",
        "1234",
    ],
)
def test__get_or_create_folder_existing(tmp_workdir, value: str):
    path = f"{tmp_workdir}/{value}"
    # Create first folder
    folder = folders._get_or_create_folder(path)
    # Repeat creation
    folder = folders._get_or_create_folder(path)
    assert isinstance(folder, Path)


@pytest.mark.parametrize(
    "key,expected",
    [
        ["environment/CHAMELEON_CACHE", "{tmp_workdir}/instance/var/cache"],
        ["db_filestorage_location", "{tmp_workdir}/instance/var/filestorage/Data.fs"],
        ["badkey", ""],
    ],
)
def test__get_str_value(expand_path, settings, key: str, expected: str):
    value = folders._get_str_value(key, settings.instance)
    assert isinstance(value, str)
    assert value == expand_path(expected)
