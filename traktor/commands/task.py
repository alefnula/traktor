from typing import Optional

import typer
from django_tea.console import output

from traktor.models import Task
from traktor.config import config
from traktor.engine import engine
from traktor.console import error_handler


app = typer.Typer(name="task", help="Task commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.db.ensure)


@app.command()
@error_handler
def list(project_id: Optional[str] = typer.Argument(None)):
    """List all tasks."""
    output(
        fmt=config.format,
        model=Task,
        objs=engine.task_list(project_id=project_id),
    )


@app.command()
@error_handler
def add(
    project_id: str,
    name: str,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    """Create a task."""
    output(
        fmt=config.format,
        model=Task,
        objs=engine.task_create(
            project_id=project_id, name=name, color=color, default=default,
        ),
    )


@app.command()
@error_handler
def update(
    project_id: str,
    task_id: str,
    name: Optional[str] = typer.Option(None, help="New task name."),
    color: Optional[str] = typer.Option(None, help="New task color"),
    default: Optional[bool] = typer.Option(
        None, help="Is this a default task."
    ),
):
    """Update a task."""
    output(
        fmt=config.format,
        model=Task,
        objs=engine.task_update(
            project_id=project_id,
            task_id=task_id,
            name=name,
            color=color,
            default=default,
        ),
    )


@app.command()
@error_handler
def delete(project_id: str, task_id: str):
    """Delete a task."""
    engine.task_delete(project_id=project_id, task_id=task_id)
