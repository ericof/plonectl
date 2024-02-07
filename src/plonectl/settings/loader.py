from dynaconf import Dynaconf
from jinja2 import Template
from pathlib import Path

import json


SETTINGS_FILES = (
    "plone.yaml",
    ".secrets.yaml",
)


def _load_settings(root_path: Path) -> dict:
    """Compute settings."""
    local_path = Path(__file__).parent
    default = local_path / "default.yaml"
    settings = Dynaconf(
        root_path=root_path,
        envvar_prefix="PLONE",
        preload=[default],
        merge_enabled=True,
        lowercase_read=False,
        settings_files=SETTINGS_FILES,
    )
    context: dict = {k.lower(): v for k, v in settings.to_dict().items()}
    target = str(Path(context["instance"]["target"]).resolve())
    context["instance"]["target"] = target
    template = Template(json.dumps(context))
    return json.loads(template.render(target=target))
