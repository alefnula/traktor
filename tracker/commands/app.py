from pathlib import Path

import typer

from tracker import errors
from tracker.engine import engine
from tracker.output import output
from tracker.config import Format, config
from tracker.models import db, Entry, Report
from tracker.decorators import error_handler
from tracker.commands.db import app as db_app
from tracker.commands.config import app as config_app
from tracker.commands.project import app as project_app
from tracker.commands.task import app as task_app
from tracker.commands.tag import app as tag_app


app = typer.Typer()
app.add_typer(db_app)
app.add_typer(config_app)
app.add_typer(project_app)
app.add_typer(task_app)
app.add_typer(tag_app)


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
@error_handler
def start(project: str, task: str):
    """Start the timer."""
    with db.session() as session:
        try:
            output(
                model=Entry,
                objs=engine.start(session=session, project=project, task=task),
            )
        except errors.TimerAlreadyRunning as e:
            typer.secho(e.message, fg=typer.colors.RED)
            output(model=Entry, objs=e.timers)


@app.command()
@error_handler
def stop():
    """Stop the timer."""
    with db.session() as session:
        output(
            model=Entry, objs=engine.stop(session=session),
        )


@app.command()
@error_handler
def status():
    """See the current running timer."""
    with db.session() as session:
        output(
            model=Entry, objs=engine.status(session=session),
        )


@app.command()
@error_handler
def today():
    """See today's timers."""
    with db.session() as session:
        output(
            model=Report, objs=engine.today(session=session),
        )


@app.command()
@error_handler
def report(days: int = typer.Argument(default=365, min=1)):
    """See the current running timer."""
    with db.session() as session:
        output(
            model=Report, objs=engine.report(session=session, days=days),
        )


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
