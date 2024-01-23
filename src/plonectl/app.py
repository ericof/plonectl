from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.users import system as user
from pathlib import Path
from Testing.makerequest import makerequest
from Zope2.Startup.run import make_wsgi_app
from zope.globalrequest import setRequest

import typer
import Zope2


def get_app_from_ctx(ctx: typer.Context) -> Zope2.app:
    """Return a Zope2 app extracting configuration from context."""
    wsgiconf = ctx.obj["wsgiconf"]
    zopeconf = ctx.obj["zopeconf"]
    return get_app(wsgiconf, zopeconf)


def get_app(wsgiconf: Path, zopeconf: Path) -> Zope2.app:
    make_wsgi_app(str(wsgiconf), str(zopeconf))
    app = Zope2.app()
    app = makerequest(app)
    app.REQUEST["PARENTS"] = [app]
    setRequest(app.REQUEST)
    newSecurityManager(None, user)
    return app


def run_script(wsgiconf: Path, zopeconf: Path, path: Path, *extra_args):
    app = get_app(wsgiconf, zopeconf)
    script_globals = {"__name__": "__main__", "app": app}
    with open(path) as script:
        scriptcode = script.read()
    exec(compile(scriptcode, path, "exec"), script_globals)


def debug(wsgiconf: Path, zopeconf: Path):
    app = get_app(wsgiconf, zopeconf)
    return app
