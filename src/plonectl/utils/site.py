from OFS.Application import Application
from plone.base.interfaces import IPloneSiteRoot
from plonectl import types
from Products.CMFPlone import factory
from Products.CMFPlone.Portal import PloneSite
from typing import List
from ZODB.broken import Broken


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


def _list_sites_from_root(
    app: Application, username: str = "admin"
) -> List[types.SiteInfo]:
    """List Plone sites."""
    from .security import authenticate_as_user

    authenticate_as_user(app, username)
    return _get_sites(app)


def list_sites(app: Application, username: str = "admin") -> List[types.SiteInfo]:
    """List Plone sites."""
    results = []
    sites = _list_sites_from_root(app, username)
    for site in sites:
        path = "/".join(site.getPhysicalPath())
        migration_tool = site.portal_migration
        versions = migration_tool.coreVersions()
        db_version = versions["Plone Instance"]
        fs_version = versions["Plone File System"]
        results.append(types.SiteInfo(path, site.title, db_version, fs_version))
    return results


def create_site(
    app: Application,
    site_id: str,
    title: str,
    language: str,
    timezone: str,
    example_content: bool,
    profiles: List[str],
    user: str,
) -> PloneSite:
    """Create a new Plone Site in this installation."""
    import transaction

    payload = {
        "site_id": site_id,
        "title": title,
        "profile_id": factory._DEFAULT_PROFILE,
        "extension_ids": profiles,
        "setup_content": example_content,
        "default_language": language,
        "portal_timezone": timezone,
    }
    with transaction.manager as tm:
        site = factory.addPloneSite(app, **payload)
        tm.setUser(user, "/acl_users")
        tm.note(f"Added site {site.id}")
    app._p_jar.sync()
    return site


def delete_site(app: Application, site_id: str, user: str) -> bool:
    import transaction

    with transaction.manager as tm:
        app.manage_delObjects([site_id])
        tm.setUser(user, "/acl_users")
        tm.note(f"Removed site {site_id}")
    app._p_jar.sync()
    return True
