from pathlib import Path
from plonectl import utils
from typing_extensions import Annotated

import sys
import typer


typer_app = typer.Typer()


@typer_app.command()
def start(ctx: typer.Context):
    """Start server."""
    from Zope2.Startup.serve import main

    wsgiconf = ctx.obj.config.wsgiconf
    sys.exit(main(argv=["plonectl", str(wsgiconf)]))


def _default_shell() -> str:
    """Return the default shell interface to use."""
    return utils.PloneShell.shells[0]


def _interface_callback(value: str):
    available_shells = utils.PloneShell.shells
    if value not in available_shells:
        raise typer.BadParameter(f"Only {', '.join(available_shells)} are supported")
    return value


def _script_callback(value: Path):
    if not value.exists():
        raise typer.BadParameter(f"Script {value} not found.")
    return value


@typer_app.command()
def shell(
    ctx: typer.Context,
    interface: Annotated[
        str,
        typer.Option(
            default_factory=_default_shell,
            help=(
                f"Which Python shell to use. Valid options are: {', '.join(utils.PloneShell.shells)}. "
                f"Default shell: {utils.PloneShell.shells[0]}. "
            ),
            show_default=False,
            callback=_interface_callback,
        ),
    ],
    site_id: Annotated[
        str,
        typer.Option(
            help="Plone site to be loaded on shell startup.",
            show_default=False,
        ),
    ] = "",
):
    """Start a shell inside the current installation.

    It is possible to choose the Python shell to be used.
    """
    shell = utils.PloneShell(ctx=ctx, shell=interface, default_site=site_id)
    # Start shell
    shell()


@typer_app.command()
def run(
    ctx: typer.Context,
    script: Annotated[
        Path,
        typer.Argument(
            help=("Path to a script to be run"),
            callback=_script_callback,
        ),
    ],
):
    """Run a script."""
    utils.run_script(ctx=ctx, path=script)
