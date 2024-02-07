from OFS.Application import Application
from plonectl import types
from ZODB.DB import DB

import pytest


@pytest.fixture(autouse=True)
def wrap_instance(tmp_workdir, default_settings):
    return tmp_workdir


@pytest.fixture
def settings(wrap_instance):
    from plonectl.settings import get_settings

    settings = get_settings(wrap_instance)
    return settings


@pytest.fixture
def instance_paths(settings) -> types.InstancePaths:
    from plonectl.instance.folders import prepare_instance_folders

    return prepare_instance_folders(settings.instance)


@pytest.fixture
def instance_config(settings, instance_paths) -> types.InstanceConfigFiles:
    from plonectl.instance import generate_config_files

    return generate_config_files(instance_paths, settings)


@pytest.fixture
def ctx(settings, instance_config):
    class MockContext:
        def __init__(self, obj):
            self.obj = obj

    ctx_obj = types.CTLContextObject(settings=settings, config=instance_config)
    ctx = MockContext(obj=ctx_obj)
    return ctx


@pytest.fixture
def zope_app(ctx, reload_code):
    from plonectl.utils import app

    wsgiconf = ctx.obj.config.wsgiconf
    zopeconf = ctx.obj.config.zopeconf
    zope_app = app.get_app(wsgiconf, zopeconf)
    yield zope_app
    reload_code()


@pytest.fixture
def number_db_txs() -> int:
    return 5


@pytest.fixture
def number_large_db_txs() -> int:
    return 200


@pytest.fixture
def add_transactions_to_app():
    import transaction

    def func(app: Application, transactions: int = 1):
        from Persistence import PersistentMapping

        for idx in range(transactions):
            with transaction.manager as tm:
                data = PersistentMapping(**{"foo": "bar", "bar": "foo"})
                app.info = data
                tm.note(f"Transaction {idx+1:02d} - Added data to App")

    return func


@pytest.fixture
def database(ctx, add_transactions_to_app, number_db_txs) -> DB:
    from plonectl.utils import db
    from plonectl.utils import get_app_from_ctx

    app = get_app_from_ctx(ctx)
    database = db.get_current_db_from_app(app)
    add_transactions_to_app(app, number_db_txs)
    return database


@pytest.fixture
def large_database(zope_app, add_transactions_to_app, number_large_db_txs) -> DB:
    from plonectl.utils import db

    database = db.get_current_db_from_app(zope_app)
    add_transactions_to_app(zope_app, number_large_db_txs)
    return database
