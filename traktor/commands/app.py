from pathlib import Path

import typer

from traktor.config import Format, config
from traktor.commands.db import app as db_app
from traktor.commands.config import app as config_app
from traktor.commands.project import app as project_app
from traktor.commands.task import app as task_app
from traktor.commands.tag import app as tag_app
from traktor.commands.timer import app as timer_app


app = typer.Typer()
app.add_typer(db_app)
app.add_typer(config_app)
app.add_typer(project_app)
app.add_typer(task_app)
app.add_typer(tag_app)
app.add_typer(timer_app)


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


@app.command()
def shell():
    """Run IPython shell with loaded configuration and models."""
    try:
        from IPython import embed
        from traktor.config import config
        from traktor.models import db, Sort, RGB, Project, Task, Tag, Entry

        embed(
            user_ns={
                "config": config,
                "db": db,
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
