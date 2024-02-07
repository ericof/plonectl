from plonectl import utils

import typer


typer_app = typer.Typer()


@typer_app.command()
def config(ctx: typer.Context):
    """Display the location of configuration files used by this instance."""
    configs = ctx.obj.config
    columns = [
        ["Config", "left"],
        ["Path", "left"],
    ]
    rows = [
        ["WSGI", utils.relative_path(configs.wsgiconf)],
        ["Zope", utils.relative_path(configs.zopeconf)],
        ["ZCML", utils.relative_path(configs.zcmlconf)],
    ]
    utils.display_table("Instance Configuration Files", columns, rows)


@typer_app.command()
def versions(ctx: typer.Context):
    """Package information."""
    columns = [
        ["Name", "left"],
        ["Package", "left"],
        ["Version", "right"],
        ["Path", "Left"],
    ]
    rows = []
    for info in utils.core_packages_info():
        path = info.path if info.path else "-"
        rows.append((info.name, info.package_name, info.version, path))
    utils.display_table("Core Packages Versions", columns, rows)
