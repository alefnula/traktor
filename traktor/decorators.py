import functools

import typer

from traktor.errors import TraktorError


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TraktorError as e:
            typer.secho(e.message, fg=typer.colors.RED)

    return wrapper
