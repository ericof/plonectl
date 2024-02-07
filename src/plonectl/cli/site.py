from plone.base.interfaces import IPloneSiteRoot
from plonectl import utils
from Products.CMFPlone.Portal import PloneSite
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
    title: str = "Plone",
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
    additional_profiles = profile if profile else []
    profiles = PROFILES[distribution]
    profiles.extend(
        [profile.strip() for profile in additional_profiles if profile.strip()]
    )
    settings = ctx.obj.settings
    user = settings.instance.initial_user_name
    app = utils.get_app_from_ctx(ctx)
    exists = site_id in app.objectIds()
    if exists:
        if not delete_existing:
            raise typer.BadParameter(f"The id {site_id} is already being used")
        utils.delete_site(app, site_id=site_id, user=user)
        typer.echo("Deleted existing site")
    typer.echo(f"Creating site {site_id} ({distribution})")
    site = utils.create_site(
        app, site_id, title, language, timezone, example_content, profiles, user
    )
    path = "/".join(site.getPhysicalPath())
    typer.echo(f"Created site {site_id} at {path}")


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


@typer_app.command(name="list")
def list_sites(ctx: typer.Context):
    """List Plone sites."""
    columns = [
        ("#", "right"),
        ("Path", "left"),
        ("Title", "left"),
        ("Database Version", "right"),
        ("Filesystem Version", "right"),
    ]
    app = utils.get_app_from_ctx(ctx)
    sites = utils.list_sites(app)
    rows = []
    for idx, site in enumerate(sites):
        rows.append((idx, site.path, site.title, site.version, site.fs_version))
    utils.display_table("Plone Sites", columns, rows)
