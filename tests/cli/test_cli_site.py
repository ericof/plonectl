import pytest


@pytest.fixture(autouse=True)
def _init(reload_code):
    """Always reload code to avoid getting another Application."""
    reload_code()


SITE_TEXT = [
    "site [OPTIONS] COMMAND [ARGS]",
    " Options ",
    " --help ",
    " Commands ",
    " create ",
    " list ",
]


@pytest.mark.parametrize("text", SITE_TEXT)
def test_cli_site_display_help(runner, cli_app, text: str):
    result = runner.invoke(cli_app, ["site"])
    assert result.exit_code == 0
    assert text in result.stdout


@pytest.mark.parametrize("text", SITE_TEXT)
def test_cli_site_help(runner, cli_app, text: str):
    result = runner.invoke(cli_app, ["site", "--help"])
    assert result.exit_code == 0
    assert text in result.stdout


@pytest.mark.parametrize(
    "site_id",
    [
        "Plone",
        "Plone2",
        "Plone3",
    ],
)
def test_cli_site_create(runner, cli_app, site_id: str):
    result = runner.invoke(cli_app, ["site", "create", site_id])
    assert result.exit_code == 0
    assert site_id in result.stdout
