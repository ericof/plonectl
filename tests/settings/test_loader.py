from pathlib import Path
from plonectl.settings import loader
from typing import Any
from typing import Callable

import pytest


def test_settings_loader_keys(tmp_workdir: Path, default_settings: Path):
    all_settings = loader._load_settings(root_path=tmp_workdir)
    assert isinstance(all_settings, dict)
    assert len(all_settings) == 2
    assert "plonectl" in all_settings
    assert "instance" in all_settings


@pytest.mark.parametrize(
    "name,category,key,value",
    [
        ["default", "plonectl", "debug_mode", False],
        ["default", "instance", "target", "{tmp_workdir}/instance"],
        ["default", "instance", "location_log", "{tmp_workdir}/instance/var/log"],
        ["default", "instance", "wsgi_listen", "localhost:8080"],
        ["default", "instance", "wsgi_fast_listen", False],
        ["default", "instance", "wsgi_threads", 4],
        ["default", "instance", "wsgi_max_request_body_size", 1073741824],
        ["default", "instance", "wsgi_clear_untrusted_proxy_headers", False],
        ["default", "instance", "initial_user_name", "admin"],
        ["default", "instance", "initial_user_password", "admin"],
        ["default", "instance", "dos_protection_available", True],
        ["default", "instance", "dos_protection_form_memory_limit", "1MB"],
        ["default", "instance", "dos_protection_form_disk_limit", "1GB"],
        ["default", "instance", "dos_protection_form_memfile_limit", "4KB"],
        ["default", "instance", "db_storage", "direct"],
        ["default", "instance", "db_cache_size", 30000],
        ["default", "instance", "db_cache_size_bytes", ""],
        ["default", "instance", "db_large_record_size", ""],
        ["default", "instance", "db_pool_size", ""],
        ["default", "instance", "db_blobs_mode", "cache"],
        [
            "default",
            "instance",
            "db_blobs_location",
            "{tmp_workdir}/instance/var/blobs",
        ],
        [
            "default",
            "instance",
            "db_filestorage_location",
            "{tmp_workdir}/instance/var/filestorage/Data.fs",
        ],
        ["default", "instance", "db_filestorage_pack_keep_old", True],
        ["default", "instance", "db_filestorage_quota", ""],
        ["default", "instance", "db_filestorage_packer", ""],
        ["default", "instance", "db_filestorage_pack_gc", ""],
        ["default", "instance", "db_relstorage", ""],
        ["default", "instance", "db_relstorage_keep_history", True],
        ["default", "instance", "db_relstorage_read_only", False],
        ["default", "instance", "db_relstorage_create_schema", True],
        ["default", "instance", "db_relstorage_commit_lock_timeout", ""],
        ["default", "instance", "db_relstorage_commit_lock_id", ""],
        ["default", "instance", "db_relstorage_blob_cache_size_check_external", ""],
        ["default", "instance", "db_relstorage_blob_chunk_size", ""],
        ["default", "instance", "db_relstorage_cache_local_mb", ""],
        ["default", "instance", "db_relstorage_cache_local_object_max", ""],
        ["default", "instance", "db_relstorage_cache_local_compression", ""],
        ["default", "instance", "db_relstorage_cache_local_dir", ""],
        ["default", "instance", "db_relstorage_cache_prefix", ""],
        ["default", "instance", "db_relstorage_replica_conf", ""],
        ["default", "instance", "db_relstorage_ro_replica_conf", ""],
        ["default", "instance", "db_relstorage_replica_revert_when_stale", ""],
        ["default", "instance", "db_relstorage_replica_timeout", ""],
        ["default", "instance", "db_relstorage_postgresql_driver", ""],
        ["default", "instance", "db_relstorage_postgresql_dsn", ""],
        ["default", "instance", "db_relstorage_mysql_driver", ""],
        ["default", "instance", "db_relstorage_mysql_parameters", {}],
        ["default", "instance", "db_relstorage_orcale_user", ""],
        ["default", "instance", "db_relstorage_orcale_password", ""],
        ["default", "instance", "db_relstorage_orcale_dsn", ""],
        ["default", "instance", "db_relstorage_sqlite3_driver", ""],
        [
            "default",
            "instance",
            "db_relstorage_sqlite3_data_dir",
            "{tmp_workdir}/instance/var/sqlite3/",
        ],
        ["default", "instance", "db_relstorage_sqlite3_gevent_yield_interval", ""],
        ["default", "instance", "db_relstorage_sqlite3_pragma", {}],
        ["default", "instance", "db_zeo_server", "localhost:8100"],
        ["default", "instance", "db_zeo_name", "1"],
        ["default", "instance", "db_zeo_client", ""],
        ["default", "instance", "db_zeo_var", ""],
        ["default", "instance", "db_zeo_cache_size", "128MB"],
        ["default", "instance", "db_zeo_username", ""],
        ["default", "instance", "db_zeo_password", ""],
        ["default", "instance", "db_zeo_realm", ""],
        ["default", "instance", "db_zeo_read_only_fallback", False],
        ["default", "instance", "db_zeo_read_only", False],
        ["default", "instance", "db_zeo_drop_cache_rather_verify", False],
        ["default", "instance", "debug_mode", False],
        ["default", "instance", "verbose_security", False],
        [
            "default",
            "instance",
            "deprecation_warnings",
            ["default", "error", "ignore", "always", "module", "once"],
        ],
        ["default", "instance", "profile_repoze", False],
        ["default", "instance", "profile_repoze_log_filename", ""],
        ["default", "instance", "profile_repoze_cachegrind_filename", ""],
        ["default", "instance", "profile_repoze_discard_first_request", ""],
        ["default", "instance", "profile_repoze_path", ""],
        ["default", "instance", "profile_repoze_flush_at_shutdown", ""],
        ["default", "instance", "profile_repoze_unwind", ""],
        ["ctl_debug", "plonectl", "debug_mode", True],
        ["data_directory", "instance", "target", "{tmp_workdir}/instance"],
        [
            "data_directory",
            "instance",
            "db_filestorage_location",
            "/data/filestorage/Data.fs",
        ],
        ["data_directory", "instance", "db_blobs_location", "/data/blobstorage"],
        ["initial_user", "instance", "initial_user_name", "root"],
        ["initial_user", "instance", "initial_user_password", "a very long password"],
    ],
)
def test_settings_loader(
    tmp_workdir: Path,
    settings_factory: Callable,
    name: str,
    category: str,
    key: str,
    value: Any,
):
    # Create settings file
    settings_factory(f"{name}.yaml")
    if isinstance(value, str) and "tmp_workdir" in value:
        value = value.format(tmp_workdir=tmp_workdir)
    all_settings = loader._load_settings(root_path=tmp_workdir)
    settings = all_settings[category]
    assert settings[key] == value
