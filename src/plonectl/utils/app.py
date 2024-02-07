from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.users import system as user
from OFS.Application import Application
from pathlib import Path
from Testing.makerequest import makerequest
from zope.globalrequest import setRequest

import hashlib
import os
import typer


_HASH_KEY = "PLONECTL_CONFIG_HASH"


def _configure_app(zopeconf: Path) -> bool:
    """Run configure_wsgi if configuration has changed."""
    from Zope2.Startup.run import configure_wsgi

    # First line always contains the header of file creation
    config = "\n".join(zopeconf.read_text().split("\n")[1:]).encode()
    hash = hashlib.md5(config).hexdigest()
    zopeconf = str(zopeconf)
    current_config = os.environ.get(_HASH_KEY, "")
    changed = current_config != zopeconf
    if changed:
        os.environ[_HASH_KEY] = hash
        configure_wsgi(zopeconf)
    return changed


def get_app(wsgiconf: Path, zopeconf: Path) -> Application:
    """Build and return a Zope2 application with the provided configuration files.

    This method also:
        - Set a request on the app
        - Create a newSecurityManager with a system user
    """
    from Zope2.Startup.run import make_wsgi_app

    import Zope2

    changed = _configure_app(zopeconf)
    if changed and Zope2._began_startup:
        from Zope2.App import startup as _startup

        _startup.app = None
        _startup.startup()
    make_wsgi_app(str(wsgiconf), str(zopeconf))
    app = Zope2.app()
    app = makerequest(app)
    app.REQUEST["PARENTS"] = [app]
    setRequest(app.REQUEST)
    newSecurityManager(None, user)
    return app


def get_app_from_ctx(ctx: typer.Context) -> Application:
    """Build and return a Zope2 application from a typer.Context."""
    wsgiconf = ctx.obj.config.wsgiconf
    zopeconf = ctx.obj.config.zopeconf
    return get_app(wsgiconf, zopeconf)


def run_script(ctx: typer.Context, path: Path, *extra_args):
    """Run a python script inside a Zope2 application."""
    app = get_app_from_ctx(ctx)
    script_globals = {"__name__": "__main__", "app": app}
    with open(path) as script:
        scriptcode = script.read()
    exec(compile(scriptcode, path, "exec"), script_globals)
