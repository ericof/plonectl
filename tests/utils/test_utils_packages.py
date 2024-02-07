from plonectl import types
from plonectl.utils import packages

import pytest


@pytest.mark.parametrize(
    "name,package_name,has_path",
    [
        ["Plone", "Plone", False],
        ["Zope", "Zope", False],
        ["plonectl", "plonectl", True],
    ],
)
def test_package_info(name: str, package_name: str, has_path: bool):
    info = packages.package_info(name, package_name)
    assert isinstance(info, types.PackageInfo)
    assert info.name == name
    assert info.package_name == package_name
    assert info.version != "unknown"
    assert (info.path is not None) is has_path


@pytest.mark.parametrize(
    "name",
    [
        "strange-package-name",
        "NotPlone123",
        "plonectl-redux",
    ],
)
def test_package_info_not_found(name):
    info = packages.package_info(name)
    assert info is None


def test_core_packages_info():
    info = packages.core_packages_info()
    assert len(info) == 7
    # First one is Python
    assert info[0].name == "Python"
