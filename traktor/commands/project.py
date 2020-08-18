from typing import Optional

import typer
from django_tea.console import command

from traktor.engine import engine
from traktor.models import Project


app = typer.Typer(name="project", help="Project commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.db.ensure)


@command(app, name="list", model=Project)
def list_projects():
    """List all projects."""
    return engine.project_list()


@command(app, model=Project)
def add(name: str, color: Optional[str] = None):
    """Create a project."""
    return engine.project_create(name=name, color=color)


@command(app, model=Project)
def update(
    project_id: str,
    name: Optional[str] = typer.Option(None, help="New project name."),
    color: Optional[str] = typer.Option(None, help="New project color"),
):
    """Update a project."""
    return engine.project_update(project_id=project_id, name=name, color=color)


@command(app)
def delete(project_id: str):
    """Delete a project."""
    engine.project_delete(project_id=project_id)
