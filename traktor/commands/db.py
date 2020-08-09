import typer

from traktor.engine import engine


app = typer.Typer(name="db", help="Database commands.")


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
