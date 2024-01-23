from AccessControl.SecurityManagement import newSecurityManager
from plone.base.interfaces import IPloneSiteRoot
from plonectl.app import get_app_from_ctx
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from Products.CMFPlone.Portal import PloneSite
from rich.console import Console
from rich.table import Table
from typing import List
from typing import Optional
from typing_extensions import Annotated
from ZODB.broken import Broken

import typer


PROFILES = {
    "volto": [
        "plone.app.caching:default",
        "plonetheme.barceloneta:default",
        "plone.volto:default",
        "plone.volto:default-homepage",
    ],
    "classic": [
        "plone.app.caching:default",
        "plonetheme.barceloneta:default",
    ],
}


def _distribution_callback(value: str):
    keys = list(PROFILES.keys())
    if value not in keys:
        raise typer.BadParameter(f"Only {', '.join(keys)} are supported")
    return value


typer_app = typer.Typer()


@typer_app.command()
def create(
    ctx: typer.Context,
    site_id: str,
    distribution: Annotated[
        str, typer.Option(callback=_distribution_callback)
    ] = "volto",
    language: str = "en",
    timezone: str = "Europe/Berlin",
    example_content: bool = True,
    profile: Annotated[Optional[List[str]], typer.Option()] = None,
    delete_existing: bool = False,
):
    """Create a new Plone Site in this installation."""
    import transaction

    additional_profiles = profile if profile else []
    profiles = PROFILES[distribution]
    profiles.extend(
        [profile.strip() for profile in additional_profiles if profile.strip()]
    )
    typer.echo(f"Creating site {site_id} - {distribution}")
    app = get_app_from_ctx(ctx)
    admin = app.acl_users.getUserById("admin")
    admin = admin.__of__(app.acl_users)
    newSecurityManager(None, admin)
    payload = {
        "title": "Plone",
        "profile_id": _DEFAULT_PROFILE,
        "extension_ids": profiles,
        "setup_content": example_content,
        "default_language": language,
        "portal_timezone": timezone,
    }
    exists = site_id in app.objectIds()
    if exists:
        if not delete_existing:
            raise typer.BadParameter(f"The id {site_id} is already being used")
        with transaction.manager as tm:
            app.manage_delObjects([site_id])
            msg = f"Removed site {site_id}"
            typer.echo(msg)
            tm.setUser("admin", "/acl_users")
            tm.note(msg)
        app._p_jar.sync()
    with transaction.manager as tm:
        site = addPloneSite(app, site_id, **payload)
        msg = f"Added site {site.id}"
        typer.echo(msg)
        tm.setUser("admin", "/acl_users")
        tm.note(msg)
    app._p_jar.sync()


def _get_sites(context) -> List[PloneSite]:
    """List Plone Sites in the context."""
    candidates = (obj for obj in context.values() if not isinstance(obj, Broken))
    results = []
    for obj in candidates:
        if obj.meta_type == "Folder":
            results.extend(_get_sites(context=obj))
        elif IPloneSiteRoot.providedBy(obj):
            results.append(obj)
        elif obj.getId() in getattr(context, "_mount_points", {}):
            results.extend(_get_sites(context=obj))
    return results


@typer_app.command()
def list(ctx: typer.Context):
    """List Plone sites."""
    app = get_app_from_ctx(ctx)
    admin = app.acl_users.getUserById("admin")
    admin = admin.__of__(app.acl_users)
    newSecurityManager(None, admin)
    console = Console()
    table = Table("#", "Path", "Title")
    results = _get_sites(app)
    for idx, site in enumerate(results):
        path = "/".join(site.getPhysicalPath())
        title = site.title
        table.add_row(f"{idx + 1:02d}", path, title)
    console.print(table)
