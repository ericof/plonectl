import pytest


INFO_TEXT = [
    "info [OPTIONS] COMMAND [ARGS]",
    " Options ",
    " --help ",
    " Commands ",
    " config ",
    " versions ",
]


@pytest.mark.parametrize("text", INFO_TEXT)
def test_cli_info_display_help(runner, cli_app, text: str):
    result = runner.invoke(cli_app, ["info"])
    assert result.exit_code == 0
    assert text in result.stdout


@pytest.mark.parametrize("text", INFO_TEXT)
def test_cli_info_help(runner, cli_app, text: str):
    result = runner.invoke(cli_app, ["info", "--help"])
    assert result.exit_code == 0
    assert text in result.stdout


@pytest.mark.parametrize(
    "command,text",
    [
        ["config", "Instance Configuration Files"],
        ["config", "instance/etc/site.zcml"],
        ["config", "instance/etc/zope.conf"],
        ["config", "instance/etc/zope.ini"],
        ["versions", "Python"],
        ["versions", "Plone"],
        ["versions", "Products.CMFPlone"],
        ["versions", "plone.api"],
        ["versions", "plone.restapi"],
        ["versions", "Zope"],
    ],
)
def test_cli_info_commands(runner, cli_app, command: str, text: str):
    result = runner.invoke(cli_app, ["info", command])
    assert result.exit_code == 0
    assert text in result.stdout
