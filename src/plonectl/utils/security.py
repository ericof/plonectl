from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.users import User
from OFS.Application import Application


def authenticate_as_user(app: Application, username: str = "admin") -> User:
    """Authenticate with a username present in the root acl_users."""
    acl_users = app.acl_users
    user = acl_users.getUserById(username)
    if not user:
        raise ValueError(
            f"User {username} not found in {'/'.join(acl_users.getPhysicalPath())}"
        )
    user = user.__of__(app.acl_users)
    newSecurityManager(None, user)
    return user
