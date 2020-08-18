from typing import Optional

import typer
from django_tea.console import command

from traktor.models import Task
from traktor.engine import engine


app = typer.Typer(name="task", help="Task commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.db.ensure)


@command(app, model=Task, name="list")
def list_tasks(project_id: Optional[str] = typer.Argument(None)):
    """List all tasks."""
    return engine.task_list(project_id=project_id)


@command(app, model=Task)
def add(
    project_id: str,
    name: str,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    """Create a task."""
    return engine.task_create(
        project_id=project_id, name=name, color=color, default=default,
    )


@command(app, model=Task)
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
    return engine.task_update(
        project_id=project_id,
        task_id=task_id,
        name=name,
        color=color,
        default=default,
    )


@command(app)
def delete(project_id: str, task_id: str):
    """Delete a task."""
    engine.task_delete(project_id=project_id, task_id=task_id)
