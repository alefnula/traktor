from typing import Optional

import typer
from tea_console.console import command

from traktor.config import config
from traktor.engine import engine
from traktor.models import User, Task


app = typer.Typer(name="task", help="Task commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.db.ensure)


@command(app, model=Task, name="list")
def list_tasks(project: Optional[str] = typer.Argument(None)):
    """List all tasks."""
    user = User.objects.get(username=config.selected_user)
    return engine.task_list(user=user, project_id=project)


@command(app, model=Task)
def add(
    project: str,
    name: str,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    """Create a task."""
    user = User.objects.get(username=config.selected_user)
    return engine.task_create(
        user=user, project_id=project, name=name, color=color, default=default,
    )


@command(app, model=Task)
def update(
    project: str,
    task_id: str,
    name: Optional[str] = typer.Option(None, help="New task name."),
    color: Optional[str] = typer.Option(None, help="New task color"),
    default: Optional[bool] = typer.Option(
        None, help="Is this a default task."
    ),
):
    """Update a task."""
    user = User.objects.get(username=config.selected_user)
    return engine.task_update(
        user=user,
        project_id=project,
        task_id=task_id,
        name=name,
        color=color,
        default=default,
    )


@command(app)
def delete(project: str, task: str):
    """Delete a task."""
    user = User.objects.get(username=config.selected_user)
    engine.task_delete(user=user, project_id=project, task_id=task)
