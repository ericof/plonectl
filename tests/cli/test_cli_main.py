import pytest


MAIN_TEXT = [
    "[OPTIONS] COMMAND [ARGS]",
    " --help ",
    "Welcome to plonectl, the Plone command line helper",
    " Options ",
    " Commands ",
    " db ",
    " info ",
    " server ",
    " site ",
    " user ",
]


@pytest.mark.parametrize("text", MAIN_TEXT)
def test_cli_no_command_display_help(runner, cli_app, text: str):
    result = runner.invoke(cli_app)
    assert result.exit_code == 0
    assert text in result.stdout


@pytest.mark.parametrize("text", MAIN_TEXT)
def test_cli_main_help(runner, cli_app, text: str):
    result = runner.invoke(cli_app, "--help")
    assert result.exit_code == 0
    assert text in result.stdout
