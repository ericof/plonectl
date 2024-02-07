from plonectl.utils import security

import pytest


@pytest.mark.parametrize("username", ["root"])
def test_authenticate_as_user(zope_app, get_current_user, username: str):
    current_user = get_current_user()
    # Authenticate
    payload = [zope_app]
    if username:
        payload.append(username)
    user = security.authenticate_as_user(*payload)
    # Get new current user
    new_user = get_current_user()
    assert current_user != new_user
    assert user == new_user


@pytest.mark.parametrize("username", ["", "plone", "admin"])
def test_authenticate_as_user_fail(zope_app, username: str):
    # Authenticate
    payload = [zope_app]
    if username:
        payload.append(username)
    else:
        # Set default value to check on exc
        username = "admin"
    with pytest.raises(ValueError) as exc:
        security.authenticate_as_user(*payload)
    assert f"User {username} not found in" in str(exc)
