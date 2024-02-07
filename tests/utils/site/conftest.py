from copy import deepcopy
from Products.CMFPlone.Portal import PloneSite
from typing import Generator

import pytest


@pytest.fixture
def plone_site_payload() -> dict:
    payload = {
        "site_id": "Plone",
        "title": "Plone",
        "profiles": [
            "plone.app.caching:default",
            "plonetheme.barceloneta:default",
            "plone.volto:default",
            "plone.volto:default-homepage",
        ],
        "example_content": True,
        "language": "en",
        "timezone": "Europe/Berlin",
        "user": "admin",
    }
    return payload


@pytest.fixture
def plone_site_factory(plone_site_payload):
    def func(app, site_id: str = "Plone") -> PloneSite:
        from plonectl.utils import site

        payload = deepcopy(plone_site_payload)
        payload["site_id"] = site_id
        return site.create_site(app, **payload)

    return func


@pytest.fixture
def plone_site(zope_app, plone_site_factory) -> Generator[PloneSite, None, None]:
    """Create a Plone site."""
    from plonectl.utils import site

    plone_site = plone_site_factory(zope_app)
    yield plone_site

    site.delete_site(zope_app, plone_site.id, "admin")
