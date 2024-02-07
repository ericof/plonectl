from plonectl import types
from plonectl.utils import site
from Products.CMFPlone.Portal import PloneSite
from typing import Generator
from typing import List

import pytest


@pytest.fixture
def plone_sites(zope_app, plone_site_factory) -> Generator[List[PloneSite], None, None]:
    sites = []
    prefix = "Plone"
    for idx in range(1, 5):
        sites.append(plone_site_factory(zope_app, f"{prefix}{idx:02d}"))
    yield sites
    # Remove sites
    for plone_site in sites:
        site.delete_site(zope_app, plone_site.id, "admin")


def test__get_sites_no_sites(zope_app):
    results = site._get_sites(zope_app)
    assert len(results) == 0


def test__get_sites(zope_app, plone_site):
    results = site._get_sites(zope_app)
    assert len(results) == 1
    assert results[0] == plone_site
    assert isinstance(results[0], PloneSite)


def test__list_sites_from_root(zope_app, plone_site):
    results = site._list_sites_from_root(zope_app, "admin")
    assert len(results) == 1
    assert results[0] == plone_site


def test_list_sites(zope_app, plone_sites):
    results = site.list_sites(zope_app)
    assert len(results) == len(plone_sites)
    site_ = results[0]
    assert isinstance(site_, types.SiteInfo)


def test_delete_site(zope_app, plone_site_factory):
    # First create the site
    plone_site = plone_site_factory(zope_app)
    results = site.list_sites(zope_app)
    assert len(results) == 1
    # Delete the site
    site.delete_site(zope_app, plone_site.id, "admin")
    results = site.list_sites(zope_app)
    assert len(results) == 0
