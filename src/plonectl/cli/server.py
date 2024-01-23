from traitlets.config import Config
from Zope2.Startup.serve import main

import IPython
import sys
import typer


typer_app = typer.Typer()


@typer_app.command()
def start(ctx: typer.Context):
    """Start server."""
    wsgiconf = ctx.obj["wsgiconf"]
    sys.exit(main(argv=["plonectl", str(wsgiconf)]))


@typer_app.command()
def shell(ctx: typer.Context):
    """Start a shell."""
    wsgiconf = ctx.obj["wsgiconf"]
    zopeconf = ctx.obj["zopeconf"]
    c = Config()
    c.InteractiveShellApp.exec_lines = [
        f"import sys; sys.path={sys.path}",
        "from plonectl.app import debug",
        f"app = debug('{wsgiconf}', '{zopeconf}')",
    ]
    c.TerminalInteractiveShell.banner1 = (
        "Starting debugger (the name 'app' is bound to the top-level Zope object)"
    )
    IPython.start_ipython(argv=[], config=c)
