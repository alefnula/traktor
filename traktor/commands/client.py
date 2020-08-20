from typing import Optional

import typer

from django_tea.console import command

from traktor.config import config
from traktor.client import Client


app = typer.Typer(name="client", help="HTTP client operations.", hidden=True)

client = Client(url=config.server_url)


# Projects


@command(app)
def project_list():
    """List all projects."""
    return client.project_list()


@command(app)
def project_get(project_id: str):
    """Get a project."""
    return client.project_get(project_id=project_id)


@command(app)
def project_create(name: str, color: str = typer.Option("#000000")):
    """Create a project."""
    return client.project_create(name=name, color=color)


@command(app)
def project_update(
    project_id: str, name: Optional[str] = None, color: Optional[str] = None
):
    """Update a project."""
    return client.project_update(project_id=project_id, name=name, color=color)


@command(app)
def project_delete(project_id: str):
    """Delete a project."""
    return client.project_delete(project_id=project_id)


# Tasks


@command(app)
def task_list(project_id: str):
    """List all tasks in a project."""
    return client.task_list(project_id=project_id)


@command(app)
def task_get(project_id: str, task_id: str):
    """Get a task."""
    return client.task_get(project_id=project_id, task_id=task_id)


@command(app)
def task_create(
    project_id: str,
    name: str,
    color: str = typer.Option("#000000"),
    default: bool = False,
):
    """Create a task."""
    return client.task_create(
        project_id=project_id, name=name, color=color, default=default
    )


@command(app)
def task_update(
    project_id: str,
    task_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    """Update a task."""
    return client.task_update(
        project_id=project_id,
        task_id=task_id,
        name=name,
        color=color,
        default=default,
    )


@command(app)
def task_delete(project_id: str, task_id: str):
    """Delete a task."""
    return client.task_delete(project_id=project_id, task_id=task_id)


# Timer


@command(app)
def timer_start(project_id: str, task_id: Optional[str] = None):
    """Start timer."""
    return client.timer_start(project_id=project_id, task_id=task_id)


@command(app)
def timer_stop():
    """Stop timer."""
    return client.timer_stop()


@command(app)
def timer_status():
    """Get timer status."""
    return client.timer_status()


@command(app)
def timer_today():
    """Get report for today."""
    return client.timer_today()


@command(app)
def timer_report(days: int = 0):
    """Get report for multiple days."""
    return client.timer_report(days=days)
