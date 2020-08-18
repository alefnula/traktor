from pathlib import Path

from django_tea.commands.db import app
from django_tea.console import command

from traktor.engine import engine


@command(app, name="export")
def export(path: Path):
    """Export database to JSON document."""
    engine.db.export(path=path)


@command(app, name="import")
def load(path: Path):
    """Import database export from JSON document."""
    engine.db.load(path=path)
