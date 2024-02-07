from rich import box
from rich.console import Console
from rich.table import Table
from typing import List


def display_table(title: str, columns: List[str], rows: List[List[str]]):
    """Print a new table"""
    console = Console()
    title = f"[bold red]{title}[/bold red]"
    table = Table(title=title, box=box.MINIMAL_DOUBLE_HEAD, row_styles=["", "dim"])
    for column, align in columns:
        column = f"[bold]{column}[/bold]"
        table.add_column(column, justify=align, vertical="middle")
    for row in rows:
        values = [str(item) for item in row]
        table.add_row(*values)
    console.print(table)
