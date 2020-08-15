import time
from typing import Optional

import typer

from traktor.output import output
from traktor.decorators import error_handler
from traktor.models import Entry, Report
from traktor.db.sync_db import sync_db as db
from traktor.engine import sync_engine as engine


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


def __output_status() -> int:
    """Output status and return number of lines printed."""
    with db.session() as session:
        objs = engine.status(session=session)
        output(model=Entry, objs=objs)
        return 6 if len(objs) > 0 else 2


@error_handler
def status(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="Show status in interactive mode."
    )
):
    """See the current running timer."""
    if interactive:
        no_lines = 0
        while True:
            try:
                if no_lines > 0:
                    print("\033[F" * no_lines)
                    for _ in range(no_lines - 1):
                        print("\033[K")
                    print("\033[F" * no_lines)

                no_lines = __output_status()
                time.sleep(1)
            except KeyboardInterrupt:
                return
    else:
        __output_status()


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
