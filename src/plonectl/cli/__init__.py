from .server import typer_app as app_server
from .site import typer_app as app_site
from .user import typer_app as app_user
from plonectl.config import config_path
from plonectl.config import instance_folder

import typer


cli = typer.Typer()


@cli.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    ctx: typer.Context,
    instance: str = "instance",
    wsgiconf: str = "etc/zope.ini",
    zopeconf: str = "etc/zope.conf",
):
    ctx.ensure_object(dict)
    instance_path = instance_folder(instance)
    ctx.obj["wsgiconf"] = config_path(instance_path, wsgiconf)
    ctx.obj["zopeconf"] = config_path(instance_path, zopeconf)


@cli.command()
def info(ctx: typer.Context):
    """Information about this instance."""
    typer.echo(f"Zope Configuration coming from {ctx.obj['zopeconf']}")


cli.add_typer(app_user, name="user", no_args_is_help=True, help="User Management")
cli.add_typer(app_site, name="site", no_args_is_help=True, help="Site Management")
cli.add_typer(app_server, name="server", no_args_is_help=True, help="Server Management")
