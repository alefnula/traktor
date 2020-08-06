import os

import typer

app = typer.Typer(name="db", help="Database commands.")


@app.command()
def revision(name: str):
    """Create a new migration."""
    os.system(f'alembic revision --autogenerate -m "{name}"')


@app.command()
def migrate(revision: str = "head"):
    """Run migrations."""
    os.system(f"alembic upgrade {revision}")


@app.command()
def reset():
    """Reset migrations - delete all tables."""
    os.system("alembic downgrade 0000")
