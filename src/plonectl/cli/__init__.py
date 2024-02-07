from .db import typer_app as app_db
from .info import typer_app as app_info
from .server import typer_app as app_server
from .site import typer_app as app_site
from .user import typer_app as app_user
from pathlib import Path
from plonectl import types

import typer


cli = typer.Typer()


@cli.callback(invoke_without_command=True, no_args_is_help=True)
def main(ctx: typer.Context):
    """Welcome to plonectl, the Plone command line helper."""
    from plonectl.instance import generate_config_files
    from plonectl.instance import prepare_instance_folders
    from plonectl.settings import get_settings

    cwd = Path.cwd()
    settings = get_settings(cwd)
    instance_paths = prepare_instance_folders(settings.instance)
    configs = generate_config_files(instance_paths, settings)

    ctx_obj = types.CTLContextObject(settings=settings, config=configs)
    ctx.obj = ctx_obj
    ctx.ensure_object(types.CTLContextObject)


cli.add_typer(
    app_db, name="db", no_args_is_help=True, help="Database Information and Actions"
)
cli.add_typer(app_info, name="info", no_args_is_help=True, help="Information")
cli.add_typer(app_user, name="user", no_args_is_help=True, help="User Management")
cli.add_typer(app_site, name="site", no_args_is_help=True, help="Site Management")
cli.add_typer(app_server, name="server", no_args_is_help=True, help="Server Management")
