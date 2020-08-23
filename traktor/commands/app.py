import typer
from pathlib import Path

from console_tea.console import command
from console_tea.enums import ConsoleFormat
from console_tea.commands.config import app as config_app

from traktor.config import config
from traktor.commands.db import app as db_app
from traktor.commands.project import app as project_app
from traktor.commands.task import app as task_app
from traktor.commands import timer
from traktor.models import Entry, Report


app = typer.Typer(name="traktor", help="Personal time tracking.")


# Add tea subcommands
app.add_typer(config_app)

# Add traktor subcommands
app.add_typer(db_app)
app.add_typer(project_app)
app.add_typer(task_app)


# Add timer commands as top level
command(app)(timer.status)
command(app, model=Entry)(timer.start)
command(app, model=Entry)(timer.stop)
command(app, model=Report)(timer.today)
command(app, model=Report)(timer.report)


@app.callback()
def callback(
    config_path: Path = typer.Option(
        default=None,
        help="Path to the configuration.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
        resolve_path=True,
    ),
    fmt: ConsoleFormat = typer.Option(
        config.format.value, "--format", help="Output format"
    ),
):
    if config_path is not None:
        config.config_path = config_path

    if config.format != fmt:
        config.format = fmt


@app.command(hidden=True)
def shell():
    """Run IPython shell with loaded configuration and models."""
    try:
        from IPython import embed
        from traktor.config import config
        from traktor.engine import engine
        from traktor.models import User, Project, Task, Entry

        embed(
            user_ns={
                "config": config,
                "engine": engine,
                "User": User,
                "Project": Project,
                "Task": Task,
                "Entry": Entry,
            },
            colors="neutral",
        )
    except ImportError:
        typer.secho("IPython is not installed", color=typer.colors.RED)
