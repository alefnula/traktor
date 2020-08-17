import typer

from django_tea.console import output
from django_tea.config import ConfigEntry

from traktor.config import config
from traktor.engine import engine
from traktor.console import error_handler

app = typer.Typer(name="config", help="Configuration set/get.")


@app.command()
def list():
    """List all configuration values."""
    output(fmt=config.format, model=ConfigEntry, objs=engine.config.list())


@app.command()
@error_handler
def set(key: str, value: str):
    """Set a configuration key."""
    output(
        fmt=config.format,
        model=ConfigEntry,
        objs=engine.config.set(key=key, value=value),
    )
