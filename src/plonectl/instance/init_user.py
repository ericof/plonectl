from binascii import b2a_base64
from hashlib import sha1
from pathlib import Path
from plonectl import types


def _encode_user_info(username: str, password: str) -> str:
    """Encode username and password."""
    pw = (b2a_base64(sha1(password.encode("utf-8")).digest())[:-1]).decode("ascii")
    return f"{username}:{{SHA}}{pw}"


def create_init_user(
    instance_paths: types.InstancePaths, settings: types.InstanceSettings
) -> Path:
    """Create inituser file for the instance."""
    instance_home = instance_paths.home
    path = instance_home / "inituser"
    if not path.exists():
        username = settings.initial_user_name
        password = settings.initial_user_password
        info = _encode_user_info(username, password)
        with open(path, "w") as fp:
            fp.write(f"{info}\n")
    return path
