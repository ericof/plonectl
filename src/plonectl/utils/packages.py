from .path import relative_path
from importlib import resources
from importlib.metadata import metadata
from importlib.metadata import PackageNotFoundError
from plonectl import types
from typing import List

import sys


PACKAGES = [
    {
        "name": "Plone",
        "pkg": [
            "Products.CMFPlone",
        ],
    },
    {
        "name": "plone.restapi",
        "pkg": [
            "plone.restapi",
        ],
    },
    {
        "name": "plone.api",
        "pkg": [
            "plone.api",
        ],
    },
    {
        "name": "CMF",
        "pkg": [
            "Products.CMFCore",
        ],
    },
    {
        "name": "Zope",
        "pkg": [
            "Zope",
        ],
    },
    {"name": "PIL", "pkg": ["Pillow", "PIL", "PILwoTK"]},
]


def package_info(name: str, package_name: str = "") -> types.PackageInfo:
    """Package Information"""
    package_name = package_name if package_name else name
    try:
        dist_info = metadata(package_name)
    except PackageNotFoundError:
        return None
    info = types.PackageInfo(name, package_name, dist_info["version"])
    try:
        path = resources.files(package_name)
    except ModuleNotFoundError:
        # This will happen with metapackages like Plone
        pass
    else:
        info.path = relative_path(path)
    return info


def core_packages_info() -> List[types.PackageInfo]:
    packages = [
        types.PackageInfo(
            "Python",
            "Python",
            f"{sys.version}({sys.platform})",
            relative_path(sys.executable),
        )
    ]

    for package in PACKAGES:
        info = None
        name = package["name"]
        for package_name in package["pkg"]:
            info = package_info(name, package_name)
            if info:
                packages.append(info)
                break
    return packages
