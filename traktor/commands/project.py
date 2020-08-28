from typing import Optional

import typer
from tea_console.console import command

from traktor.config import config
from traktor.engine import engine
from traktor.models import User, Project


app = typer.Typer(name="project", help="Project commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.db.ensure)


@command(app, name="list", model=Project)
def projects_list():
    """List all projects."""
    user = User.objects.get(username=config.selected_user)
    return engine.project_list(user)


@command(app, name="create", model=Project)
def project_create(name: str, color: Optional[str] = None):
    """Create a project."""
    user = User.objects.get(username=config.selected_user)
    return engine.project_create(user=user, name=name, color=color)


@command(app, name="update", model=Project)
def project_update(
    project: str,
    name: Optional[str] = typer.Option(None, help="New project name."),
    color: Optional[str] = typer.Option(None, help="New project color"),
):
    """Update a project."""
    user = User.objects.get(username=config.selected_user)
    return engine.project_update(
        user=user, project_id=project, name=name, color=color
    )


@command(app, name="delete")
def project_delete(project: str):
    """Delete a project."""
    user = User.objects.get(username=config.selected_user)
    engine.project_delete(user=user, project_id=project)
