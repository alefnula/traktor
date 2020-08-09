from typing import Optional

import typer

from traktor import errors
from traktor.engine import engine
from traktor.output import output
from traktor.decorators import error_handler
from traktor.models import db, Entry, Report


app = typer.Typer(name="timer", help="Start/stop timer and reports.")


@app.command()
@error_handler
def start(project: str, task: Optional[str] = typer.Argument(None)):
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
