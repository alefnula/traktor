import typer

from traktor.output import output
from traktor.engine import sync_engine as engine
from traktor.models import ConfigEntry, ConfigKey

app = typer.Typer(name="config", help="Configuration set/get.", hidden=True)


@app.command()
def list():
    """List all configuration values."""
    output(model=ConfigEntry, objs=engine.config_list())


@app.command()
def set(key: ConfigKey, value: str):
    """Set a configuration key."""
    output(model=ConfigEntry, objs=engine.config_set(key=key, value=value))
