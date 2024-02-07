from pathlib import Path
from typing import Generator

import importlib
import pytest
import shutil


@pytest.fixture
def reload_code():
    """Reload Zope2, ZODB and transaction codebases."""

    def func():
        to_reload = [
            ("transaction",),
            ("Zope2",),
            (".startup", "Zope2.App"),
            (".app", "plonectl.utils"),
            (".DB", "ZODB"),
            (".Connection", "ZODB"),
        ]
        for args in to_reload:
            module = importlib.import_module(*args)
            importlib.reload(module=module)

    return func


@pytest.fixture
def workdir_factory(monkeypatch, tmp_path) -> Path:
    def func() -> Path:
        path: Path = tmp_path
        if path.exists():
            shutil.rmtree(path)
        path.mkdir()
        # Used for cli output
        monkeypatch.setenv("COLUMNS", "180")
        monkeypatch.setenv("LINES", "40")
        # To avoid reusing Zope instance
        monkeypatch.delenv("CLIENT_HOME", raising=False)
        monkeypatch.delenv("INSTANCE_HOME", raising=False)
        monkeypatch.chdir(path)
        settings = path / "plone.yaml"
        settings.write_text("---")
        return path

    return func


@pytest.fixture
def tmp_workdir(workdir_factory) -> Generator:
    path = workdir_factory()
    yield path
    # shutil.rmtree(path)


@pytest.fixture
def settings_factory(tmp_workdir) -> Path:
    """Create a settings file in the temporary workdir."""
    resources_folder = Path(__file__).parent / "_resources"

    def func(name: str, output: str = "plone.yaml") -> Path:
        src = resources_folder / name
        dst = f"{tmp_workdir}/{output}"
        with open(dst, "w") as fout:
            fout.write(src.read_text())
        return dst

    return func


@pytest.fixture
def default_settings(settings_factory) -> Path:
    """Return an empty settings file."""
    path = settings_factory("default.yaml")
    return path


@pytest.fixture
def scripts_factory(tmp_workdir) -> Path:
    """Add a script to the cwd."""
    resources_folder = Path(__file__).parent / "_resources"

    def func(name: str, output: str = "") -> Path:
        output = output if output else name
        src = resources_folder / name
        dst = f"{tmp_workdir}/{output}"
        # Copy only if src exists, otherwise return the dst path
        if src.exists():
            with open(dst, "w") as fout:
                fout.write(src.read_text())
        return dst

    return func


@pytest.fixture
def expand_path(tmp_workdir) -> str:
    """Expand a path inside tmp_workdir."""

    def func(path: str) -> str:
        return path.format(tmp_workdir=tmp_workdir)

    return func
