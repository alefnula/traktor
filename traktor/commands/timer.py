import time
from typing import Optional

import typer
from tea_console.console import output

from traktor.config import config
from traktor.engine import engine
from traktor.models import User, Entry


def start(project: str, task: Optional[str] = typer.Argument(None)):
    """Start the timer."""
    user = User.objects.get(username=config.selected_user)
    return engine.timer_start(user=user, project_id=project, task_id=task)


def stop():
    """Stop the timer."""
    user = User.objects.get(username=config.selected_user)
    return engine.timer_stop(user=user)


def __output_status(user: User) -> int:
    """Output status and return number of lines printed."""
    timer = engine.timer_status(user=user)
    output(fmt=config.format, model=Entry, objs=timer)
    return 2 if timer is None else 6


def status(
    interactive: bool = typer.Option(
        False, "-i", "--interactive", help="Show status in interactive mode."
    )
):
    """See the current running timer."""
    user = User.objects.get(username=config.selected_user)
    if interactive:
        no_lines = 0
        while True:
            try:
                if no_lines > 0:
                    print("\033[F" * no_lines)
                    for _ in range(no_lines - 1):
                        print("\033[K")
                    print("\033[F" * no_lines)

                no_lines = __output_status(user=user)
                time.sleep(1)
            except KeyboardInterrupt:
                return
    else:
        __output_status(user=user)


def today():
    """See today's timers."""
    user = User.objects.get(username=config.selected_user)
    return engine.timer_today(user=user)


def report(days: int = typer.Argument(default=0, min=0)):
    """See the current running timer.

    If days is 0 that means whole history.
    """
    user = User.objects.get(username=config.selected_user)
    return engine.timer_report(user=user, days=days)
