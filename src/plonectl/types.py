from dataclasses import dataclass
from dataclasses import field
from dataclasses import is_dataclass
from datetime import datetime
from pathlib import Path
from typing import TypeAlias
from typing import Union


StrPath: TypeAlias = Union[str, Path]


def nested_deco(*args, **kwargs):
    def wrapper(check_class):
        # passing class to investigate
        check_class = dataclass(check_class, **kwargs)
        o_init = check_class.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                # getting field type
                ft = check_class.__annotations__.get(name, None)

                if is_dataclass(ft) and isinstance(value, dict):
                    obj = ft(**value)
                    kwargs[name] = obj
                o_init(self, *args, **kwargs)

        check_class.__init__ = __init__

        return check_class

    return wrapper(args[0]) if args else wrapper


@dataclass
class PloneCTLSettings:
    """Settings used by plonectl."""

    debug_mode: bool


@dataclass
class ZCMLSettings:
    """Load ZCML settings."""

    package_metas: field(default_factory=list)
    package_includes: field(default_factory=list)
    package_overrides: field(default_factory=list)
    locales_directory_location: str
    include_file_location: str
    overrides_file_location: str
    resources_directory_location: str


@nested_deco
class InstanceSettings:
    """Zope / Plone Instance settings."""

    target: str
    location_clienthome: str
    location_log: str
    wsgi_listen: str
    wsgi_fast_listen: bool
    wsgi_threads: int
    wsgi_max_request_body_size: int
    wsgi_clear_untrusted_proxy_headers: bool
    environment: field(default_factory=dict)
    initial_user_name: str
    initial_user_password: str
    load_zcml: ZCMLSettings

    dos_protection_available: bool
    dos_protection_form_memory_limit: str
    dos_protection_form_disk_limit: str
    dos_protection_form_memfile_limit: str

    db_storage: str
    db_cache_size: int
    db_cache_size_bytes: int
    db_large_record_size: int
    db_pool_size: int
    db_blobs_mode: str
    db_blobs_location: str
    db_filestorage_location: str
    db_filestorage_pack_keep_old: bool
    db_filestorage_quota: str
    db_filestorage_packer: str
    db_filestorage_pack_gc: str
    db_relstorage: str
    db_relstorage_keep_history: bool
    db_relstorage_read_only: bool
    db_relstorage_create_schema: bool
    db_relstorage_commit_lock_timeout: str
    db_relstorage_commit_lock_id: str
    db_relstorage_blob_cache_size_check_external: str
    db_relstorage_blob_chunk_size: str
    db_relstorage_cache_local_mb: str
    db_relstorage_cache_local_object_max: str
    db_relstorage_cache_local_compression: str
    db_relstorage_cache_local_dir: str
    db_relstorage_cache_prefix: str
    db_relstorage_replica_conf: str
    db_relstorage_ro_replica_conf: str
    db_relstorage_replica_revert_when_stale: str
    db_relstorage_replica_timeout: str
    db_relstorage_postgresql_driver: str
    db_relstorage_postgresql_dsn: str
    db_relstorage_mysql_driver: str
    db_relstorage_mysql_parameters: field(default_factory=dict)
    db_relstorage_orcale_user: str
    db_relstorage_orcale_password: str
    db_relstorage_orcale_dsn: str
    db_relstorage_sqlite3_driver: str
    db_relstorage_sqlite3_data_dir: str
    db_relstorage_sqlite3_gevent_yield_interval: str
    db_relstorage_sqlite3_pragma: field(default_factory=dict)
    db_zeo_server: str
    db_zeo_name: str
    db_zeo_client: str
    db_zeo_var: str
    db_zeo_cache_size: str
    db_zeo_username: str
    db_zeo_password: str
    db_zeo_realm: str
    db_zeo_read_only_fallback: bool
    db_zeo_read_only: bool
    db_zeo_drop_cache_rather_verify: bool
    debug_mode: bool
    verbose_security: bool
    deprecation_warnings: field(default_factory=list)
    profile_repoze: bool
    profile_repoze_log_filename: str
    profile_repoze_cachegrind_filename: str
    profile_repoze_discard_first_request: str
    profile_repoze_path: str
    profile_repoze_flush_at_shutdown: str
    profile_repoze_unwind: str


@nested_deco
class LoadedSettings:
    """PloneCTL instance."""

    plonectl: PloneCTLSettings
    instance: InstanceSettings


@dataclass
class InstanceConfigFiles:
    """Instance configuration files."""

    zcmlconf: Path
    wsgiconf: Path
    zopeconf: Path


@dataclass
class CTLContextObject:
    """Context object used by plonectl."""

    settings: LoadedSettings
    config: InstanceConfigFiles


@dataclass
class InstancePaths:
    home: Path
    client_home: Path
    config: Path


@dataclass
class PackageInfo:
    name: str
    package_name: str
    version: str = "unknown"
    path: Path = None


@dataclass
class DBReport:
    db_name: str
    storage_type: str
    undo_support: bool
    objects: int
    size: int
    cache_size_objects: int
    cache_length_objects: int
    cache_length_bytes: int


@dataclass
class DBTransaction:
    time: datetime
    description: str
    size: int
    user: str


@dataclass
class SiteInfo:
    path: str
    title: str
    version: str
    fs_version: str
