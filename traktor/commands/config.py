import pytz
import typer

from traktor.config import config, Format

app = typer.Typer(name="config", help="Configuration set/get.")


@app.command()
def list():
    """List all configuration values."""
    print(f"format     :   {config.format.value}")
    print(f"db_path    :   {config.db_path}")
    print(f"timezone   :   {config.timezone.zone}")


@app.command()
def set(key: str, value: str):
    if key == "format":
        try:
            config.format = Format(value)
        except Exception:
            valid_values = ", ".join([f.value for f in Format])
            typer.secho(
                f"Invalid format value: {value}. Valid values: {valid_values}",
                fg=typer.colors.RED,
            )
    elif key == "db_path":
        config.db_path = value
    elif key == "timezone":
        try:
            config.timezone = pytz.timezone(value)
        except Exception:
            typer.secho(f"Invalid timezone: {value}", fg=typer.colors.RED)
    else:
        typer.secho(f"Invalid configuration key: {key}", fg=typer.colors.RED)

    config.save()
