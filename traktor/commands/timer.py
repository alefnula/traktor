from typing import Optional

import typer

from traktor.engine import engine
from traktor.output import output
from traktor.decorators import error_handler
from traktor.models import db, Entry, Report


@error_handler
def start(project: str, task: Optional[str] = typer.Argument(None)):
    """Start the timer."""
    with db.session() as session:
        output(
            model=Entry,
            objs=engine.start(session=session, project=project, task=task),
        )


@error_handler
def stop():
    """Stop the timer."""
    with db.session() as session:
        output(
            model=Entry, objs=engine.stop(session=session),
        )


@error_handler
def status():
    """See the current running timer."""
    with db.session() as session:
        output(
            model=Entry, objs=engine.status(session=session),
        )


@error_handler
def today():
    """See today's timers."""
    with db.session() as session:
        output(
            model=Report, objs=engine.today(session=session),
        )


@error_handler
def report(days: int = typer.Argument(default=0, min=0)):
    """See the current running timer.

    If days is 0 that means whole history.
    """
    with db.session() as session:
        output(
            model=Report, objs=engine.report(session=session, days=days),
        )
