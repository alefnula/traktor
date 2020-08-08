import os
import subprocess

import typer

app = typer.Typer(name="db", help="Database commands.")


@app.command()
def revision(name: str):
    """Create a new migration."""
    os.system(f'alembic revision --autogenerate -m "{name}"')


@app.command()
def migrate(revision: str = typer.Argument(default="head")):
    """Run migrations."""
    if revision == "head":
        direction = "upgrade"
    else:
        destination = int(revision, 10)
        current = int(subprocess.check_output(["alembic", "current"])[:4], 10)
        if destination > current:
            direction = "upgrade"
        else:
            direction = "downgrade"

    os.system(f"alembic {direction} {revision}")


@app.command()
def reset():
    """Reset migrations - delete all tables."""
    os.system("alembic downgrade 0000")
