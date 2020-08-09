import json
import functools

from rich import print

from traktor.config import config
from traktor.errors import TraktorError


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TraktorError as e:
            if config.format == config.Format.text:
                print(f"[red]{e.message}[/red]")
            elif config.format == config.Format.json:
                print(json.dumps({"error": e.message}))

    return wrapper
