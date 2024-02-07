from plonectl import types
from plonectl.utils import db
from relstorage.storage import RelStorage
from typing import Any
from ZODB.DB import DB

import pytest


def test_get_current_db_from_app(zope_app):
    database = db.get_current_db_from_app(zope_app)
    assert isinstance(database, DB)
    assert isinstance(database.storage, RelStorage)


def test_get_current_db_from_ctx(ctx):
    database = db.get_current_db_from_ctx(ctx)
    assert isinstance(database, DB)
    assert isinstance(database.storage, RelStorage)


def test_format_storage(database):
    name = db.format_storage(database.storage)
    assert isinstance(name, str)
    assert name == "RelStorage"


def test_transactions_from_db(database):
    transactions = db.transactions_from_db(database)
    assert isinstance(transactions, list)
    tx = transactions[0]
    assert isinstance(tx, types.DBTransaction)


@pytest.mark.parametrize(
    "attr,expected",
    [
        ["db_name", "RelStorage: "],
        ["storage_type", "RelStorage"],
        ["undo_support", True],
    ],
)
def test_create_db_report(database, attr: str, expected: Any):
    report = db.create_db_report(database)
    assert isinstance(report, types.DBReport)
    value = getattr(report, attr)
    if isinstance(expected, str):
        assert expected in value
    elif isinstance(expected, bool):
        assert value is expected
    else:
        assert getattr(report, attr) == expected


@pytest.mark.parametrize(
    "attr,instance",
    [
        ["db_name", str],
        ["storage_type", str],
        ["undo_support", bool],
        ["objects", int],
        ["size", int],
        ["cache_size_objects", int],
        ["cache_length_objects", int],
        ["cache_length_bytes", int],
    ],
)
def test_create_db_report_instances(database, attr: str, instance: Any):
    report = db.create_db_report(database)
    assert isinstance(getattr(report, attr), instance)


def test_pack_db(large_database, number_large_db_txs):
    log = db.transactions_from_db(large_database, last=number_large_db_txs)
    before = len(log)
    # Pack database
    db.pack_db(large_database, 0.0)
    # Should reduce
    after = len(db.transactions_from_db(large_database, last=number_large_db_txs))
    assert before > after
    # No transactions here
    assert after == 0
