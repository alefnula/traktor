from pathlib import Path

import typer

from traktor.db.sync_db import sync_db as db
from traktor.engine import sync_engine as engine


app = typer.Typer(name="db", help="Database commands.", hidden=True)


@app.command()
def revision(name: str):
    """Create a new migration."""
    engine.db_revision(revision=name)


@app.command()
def migrate(revision: str = typer.Argument(default="head")):
    """Run migrations."""
    engine.db_migrate(revision=revision)


@app.command()
def reset():
    """Reset migrations - delete all tables."""
    engine.db_reset()


@app.command()
def export(path: Path):
    """Export database to JSON document."""
    with db.session() as session:
        engine.export(session=session, path=path)
