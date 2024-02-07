from AccessControl.SecurityManagement import getSecurityManager

import pytest


@pytest.fixture
def get_current_user():
    def func():
        sm = getSecurityManager()
        return sm.getUser()

    return func
