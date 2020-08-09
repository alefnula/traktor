import functools

import typer

from tracker.output import output
from tracker.errors import TrackerError


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TrackerError as e:
            typer.secho(e.message, fg=typer.colors.RED)
            if e.rich is not None:
                output(model=e.rich.model, objs=e.rich.objects)

    return wrapper
