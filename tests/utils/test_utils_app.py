from OFS.Application import Application
from pathlib import Path
from plonectl.utils import app
from ZPublisher.HTTPRequest import HTTPRequest

import pytest


@pytest.fixture
def hello_app(scripts_factory) -> Path:
    return scripts_factory("hello_app.py")


def test_get_app(ctx):
    wsgiconf = ctx.obj.config.wsgiconf
    zopeconf = ctx.obj.config.zopeconf
    result = app.get_app(wsgiconf, zopeconf)
    assert isinstance(result, Application)


def test_get_app_from_ctx(ctx):
    result = app.get_app_from_ctx(ctx)
    assert isinstance(result, Application)


def test_app_has_request_set(zope_app):
    request = zope_app.REQUEST
    assert isinstance(request, HTTPRequest)
    assert "PARENTS" in request
    assert request["PARENTS"] == [zope_app]


def test_run_script(ctx, hello_app, capsys):
    # Run script
    app.run_script(ctx, hello_app)
    captured = capsys.readouterr()
    assert "Hello <Application at >" in captured.out


@pytest.mark.parametrize(
    "script_name,exception,msg",
    [
        ("foo.py", FileNotFoundError, "No such file or directory"),
        ("hello_app.sh", SyntaxError, "invalid syntax"),
    ],
)
def test_run_script_fail(ctx, scripts_factory, script_name: str, exception, msg: str):
    script = scripts_factory(script_name)
    with pytest.raises(exception) as exc:
        app.run_script(ctx, script)
    assert msg in str(exc)
