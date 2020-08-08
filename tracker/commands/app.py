from pathlib import Path

import typer

from tracker.config import Format, config
from tracker.commands.db import app as db_app
from tracker.commands.config import app as config_app
from tracker.commands.project import app as project_app


app = typer.Typer()
app.add_typer(db_app)
app.add_typer(config_app)
app.add_typer(project_app)


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
    profile: str = typer.Option(None, help="Configuration profile."),
    fmt: Format = typer.Option(
        default=config.format.value, help="Output format"
    ),
    db_path: Path = typer.Option(
        default=config.db_path,
        help="Path to the database.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
):
    if config_path is not None:
        config.config_path = config_path
    if profile is not None:
        config.profile = profile

    config.load()

    if config.format != fmt:
        config.format = fmt

    if config.db_path != str(db_path.absolute()):
        config.db_path = str(db_path.absolute())


@app.command()
def shell():
    """Run IPython shell with loaded configuration and models."""
    try:
        from IPython import embed
        from tracker.config import config
        from tracker.models import db, Sort, RGB, Project, Task, Tag, Entry

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
