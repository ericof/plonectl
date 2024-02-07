from .packages import package_info
from OFS.Application import Application
from Products.CMFPlone.Portal import PloneSite
from typing import Dict
from typing import List
from zope.component.hooks import setSite

import typer


class PloneShell:
    ctx: typer.Context
    shell: str
    startup_msg: str = (
        "Starting debugger console\n" " - 'app' is bound to the top-level Zope object"
    )
    zope_app: Application = None
    sites: Dict[str, PloneSite] = None
    _site_id: str = ""

    def __init__(self, ctx: typer.Context, shell: str = "", default_site: str = ""):
        from .app import get_app_from_ctx
        from .site import _list_sites_from_root

        self.ctx = ctx
        self.shell = shell
        self.zope_app = get_app_from_ctx(self.ctx)
        sites = _list_sites_from_root(self.zope_app)
        self.sites = {site.id: site for site in sites}
        if default_site:
            self._site_id = default_site if default_site in self.sites else ""
        else:
            self._site_id = list(self.sites.keys())[0] if len(self.sites) == 1 else ""

    @classmethod
    @property
    def shells(cls) -> List[str]:
        interfaces = []
        for package in ["bpython", "IPython"]:
            info = package_info(package, package)
            if info:
                interfaces.append(package.lower())

        # Add the default shell
        interfaces.append("python")
        return interfaces

    def _get_locals(self) -> dict:
        """Return locals to be used by the new shell."""
        locals = {
            "app": self.zope_app,
        }
        if self._site_id:
            site = self.sites[self._site_id]
            path = "/".join(site.getPhysicalPath())
            setSite(site)
            locals["site"] = site
            self.startup_msg = (
                f"{self.startup_msg}\n - 'site' is bound to the Plone Site at {path}"
            )
        return locals

    def python(self):
        """Start a shell with python."""
        import code

        console = code.InteractiveConsole(self._get_locals())
        console.interact(banner=self.startup_msg)

    def bpython(self):
        """Start a shell with bpython."""
        import bpython

        args = ["-i", "-q"]
        bpython.embed(self._get_locals(), args=args, banner=self.startup_msg)

    def ipython(self):
        """Start a shell with ipython."""
        from traitlets.config import Config

        import IPython

        locals = self._get_locals()
        c = Config()
        c.TerminalInteractiveShell.banner1 = self.startup_msg
        IPython.start_ipython(argv=[], user_ns=locals, config=c)

    def __call__(self):
        shell = self.shell
        available_shells = [shell] if shell else self.shells

        for shell in available_shells:
            try:
                return getattr(self, shell)()
            except ImportError:
                pass
        raise typer.BadParameter(f"Couldn't import {shell} interface.")
