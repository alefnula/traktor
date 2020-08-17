from pathlib import Path

from django_tea.commands.db import app

from traktor.engine import engine


@app.command(name="export")
def export(path: Path):
    """Export database to JSON document."""
    engine.db.export(path=path)


@app.command(name="import")
def load(path: Path):
    """Import database export from JSON document."""
    engine.db.load(path=path)
