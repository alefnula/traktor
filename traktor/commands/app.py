from pathlib import Path

import typer

from traktor.config import Format, config
from traktor.commands import timer
from traktor.commands.db import app as db_app
from traktor.commands.config import app as config_app
from traktor.commands.project import app as project_app
from traktor.commands.task import app as task_app
from traktor.commands.tag import app as tag_app
from traktor.commands.server import app as server_app
from traktor.commands.client import app as client_app


app = typer.Typer()

# Add timer commands
app.command()(timer.start)
app.command()(timer.stop)
app.command()(timer.status)
app.command()(timer.today)
app.command()(timer.report)

# Add other apps
app.add_typer(db_app)
app.add_typer(config_app)
app.add_typer(project_app)
app.add_typer(task_app)
app.add_typer(tag_app)
app.add_typer(server_app)
app.add_typer(client_app)


@app.callback()
def callback(
    config_path: Path = typer.Option(
        default=None,
        help="Path to the configuration.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    format: Format = typer.Option(
        default=config.format.value, help="Output format"
    ),
    db_path: Path = typer.Option(
        default=config.db_path,
        help="Path to the database.",
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    if config_path is not None:
        config.config_path = config_path

    config.load()

    if config.format != format:
        config.format = format

    if config.db_path != str(db_path.absolute()):
        config.db_path = str(db_path.absolute())


@app.command(hidden=True)
def shell():
    """Run IPython shell with loaded configuration and models."""
    try:
        from IPython import embed
        from traktor.config import config
        from traktor.engine import sync_engine
        from traktor.db.sync_db import sync_db
        from traktor.models import (
            Sort,
            RGB,
            Project,
            Task,
            Tag,
            Entry,
        )

        embed(
            user_ns={
                "config": config,
                "db": sync_db,
                "engine": sync_engine,
                "Sort": Sort,
                "RGB": RGB,
                "Project": Project,
                "Task": Task,
                "Tag": Tag,
                "Entry": Entry,
            },
            colors="neutral",
        )
    except ImportError:
        typer.secho("IPython is not installed", color=typer.colors.RED)
