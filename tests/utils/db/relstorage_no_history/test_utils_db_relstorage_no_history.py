from plonectl import types
from plonectl.utils import db

import pytest


def test_transactions_from_db(database):
    with pytest.raises(ValueError) as exc:
        db.transactions_from_db(database)
    assert "Database does not support history." in str(exc)


def test_create_db_report_no_undo(database):
    report = db.create_db_report(database)
    assert isinstance(report, types.DBReport)
    assert report.undo_support is False


def test_pack_db(large_database):
    with pytest.raises(ValueError) as exc:
        db.pack_db(large_database, 0.0)
    assert "Database does not support history." in str(exc)
