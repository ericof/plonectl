from datetime import datetime
from plonectl import utils
from typing_extensions import Annotated

import typer


typer_app = typer.Typer()


@typer_app.command()
def info(ctx: typer.Context):
    """Database information."""
    db = utils.get_current_db_from_ctx(ctx)
    columns = [
        ("Item", "left"),
        ("Value", "right"),
    ]
    rows = [
        ["Database", db.getName()],
        ["Storage Type", utils.format_storage(db.storage)],
        ["Undo support", "Enabled" if db.supportsUndo() else "Disabled"],
        ["Objects", utils.format_int(db.objectCount())],
        ["Size", utils.format_bytes(db.getSize())],
        ["Cache Size (objects)", utils.format_int(db.getCacheSize())],
        ["Cache Length (objects)", utils.format_int(db.cacheSize())],
        ["Cache Length (bytes)", utils.format_bytes(db.getCacheSizeBytes())],
    ]
    utils.display_table("Database Information", columns, rows)


@typer_app.command()
def transactions(ctx: typer.Context, first: int = 0, last: int = 20):
    """List the last transactions in the database."""
    db = utils.get_current_db_from_ctx(ctx)
    if not db.supportsUndo():
        typer.echo("Database does not support undo.")
    else:
        columns = (
            ("Date", "right"),
            ("Description", "left"),
            ("Size", "right"),
            ("User", "left"),
        )
        rows = []
        transactions = db.undoLog(first, last)
        for transaction in transactions:
            time = datetime.fromtimestamp(transaction["time"])
            description = transaction["description"].decode()
            size = utils.format_bytes(transaction["size"])
            user = transaction["user_name"].decode()
            user = user if user else "Zope"
            rows.append((f"{time:%Y-%m-%d %H:%M:%S}", description, size, user))
        utils.display_table("Transaction Log", columns, rows)


@typer_app.command()
def pack(
    ctx: typer.Context,
    days: Annotated[
        float,
        typer.Option(
            prompt=True,
            min=0.0,
            help="Keep transactions newer than this number of days.",
        ),
    ] = 1.0,
):
    """Remove old transactions from the database."""
    db = utils.get_current_db_from_ctx(ctx)
    curr_size = utils.format_bytes(db.getSize())
    curr_obj = utils.format_int(db.objectCount())
    utils.pack_db(db, days)
    new_size = utils.format_bytes(db.getSize())
    new_obj = utils.format_int(db.objectCount())
    columns = [
        ("Stat", "Left"),
        ("Before", "right"),
        ("After", "right"),
    ]
    rows = [
        ["Size", curr_size, new_size],
        ["Objects", curr_obj, new_obj],
    ]
    utils.display_table("Database Stats", columns, rows)
