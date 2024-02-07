from datetime import datetime
from OFS.Application import Application
from plonectl import types
from typing import List
from ZODB.interfaces import IDatabase
from ZODB.interfaces import IStorage

import typer


def format_storage(storage: IStorage) -> str:
    """Return a human friendly name for the ZODB Storage in use."""
    return storage.__class__.__name__


def get_current_db_from_app(app: Application) -> IDatabase:
    """Return the current Database on a Zope2 Application."""
    db = app._p_jar.db()
    return db


def get_current_db_from_ctx(ctx: typer.Context) -> IDatabase:
    """Return the current Database on a Zope2 Application."""
    from .app import get_app_from_ctx

    app = get_app_from_ctx(ctx)
    return get_current_db_from_app(app)


def transactions_from_db(
    database: IDatabase, first: int = 0, last: int = 20
) -> List[types.DBTransaction]:
    transactions = []
    if not database.supportsUndo():
        raise ValueError("Database does not support history.")
    raw_txs = database.undoLog(first, last)
    for tx in raw_txs:
        time = datetime.fromtimestamp(tx["time"])
        description = tx["description"]
        size = tx.get("size", 0)  # Some storages do not save the size
        user = tx["user_name"]
        user = user if user else "Zope"
        transactions.append(types.DBTransaction(time, description, size, user))
    return transactions


def create_db_report(database: IDatabase) -> types.DBReport:
    """Report of Database."""
    report = types.DBReport(
        db_name=database.getName(),
        storage_type=format_storage(database.storage),
        undo_support=bool(database.supportsUndo()),
        objects=database.objectCount(),
        size=database.getSize(),
        cache_size_objects=database.getCacheSize(),
        cache_length_objects=database.cacheSize(),
        cache_length_bytes=database.getCacheSizeBytes(),
    )
    return report


def pack_db(database: IDatabase, days: float = 1.0) -> None:
    """Pack a database."""
    report = create_db_report(database)
    if not report.undo_support:
        raise ValueError("Database does not support history.")
    database.pack(days=days)
