from pathlib import Path

import typer
from tea_console.console import command

from traktor.engine import engine


app = typer.Typer(name="db", help="Database export/import.")


@command(app, name="export")
def export(path: Path):
    """Export database to JSON document."""
    engine.db.export(path=path)


@command(app, name="import")
def load(path: Path):
    """Import database export from JSON document."""
    engine.db.load(path=path)
