from datetime import datetime
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape
from jinja2 import Template
from pathlib import Path
from plonectl import types


CONFIGS = (
    ("zcmlconf", "site.zcml"),
    ("wsgiconf", "zope.ini"),
    ("zopeconf", "zope.conf"),
)


def _create_jinja_environment() -> Environment:
    return Environment(
        loader=PackageLoader("plonectl", "instance/templates"),
        autoescape=select_autoescape(),
    )


class ConfigFileWriter:
    """Configuration file writer."""

    context: dict = None
    env: Environment = None
    name: str = ""
    output: Path = None

    def __init__(self, name: str, context: dict, env: Environment, output: Path):
        self.context = context
        self.name = name
        self.env = env
        self.output = output

    @property
    def template(self) -> Template:
        """Return the Jinja2 Template to be used."""
        template_name = self.name.replace(".", "_")
        return self.env.get_template(f"{template_name}.j2")

    def __call__(self) -> Path:
        """Generate config file."""
        debug = {"app": "plonectl", "date": f"{datetime.now()}"}
        config = self.template.render(context=self.context, debug=debug)
        path = (self.output / self.name).resolve()
        with open(path, "w") as fh:
            fh.write(config)
        return path


def generate_config_files(
    instance_paths: types.InstancePaths,
    settings: types.LoadedSettings,
) -> types.InstanceConfigFiles:
    """Generate configuration files from settings."""

    files = {}
    instance_settings = settings.instance
    configs_folder = instance_paths.config
    env = _create_jinja_environment()
    for config_id, name in CONFIGS:
        writer = ConfigFileWriter(
            name, context=instance_settings, env=env, output=configs_folder
        )
        files[config_id] = writer()
    return types.InstanceConfigFiles(**files)
