from typing import Optional

import typer
from django_tea.console import output


from traktor.config import config
from traktor.engine import engine
from traktor.models import Project
from traktor.console import error_handler


app = typer.Typer(name="project", help="Project commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.db.ensure)


@app.command()
@error_handler
def list():
    """List all projects."""
    output(
        fmt=config.format, model=Project, objs=engine.project_list(),
    )


@app.command()
@error_handler
def add(name: str, color: Optional[str] = None):
    """Create a project."""
    output(
        fmt=config.format,
        model=Project,
        objs=engine.project_create(name=name, color=color),
    )


@app.command()
@error_handler
def update(
    project_id: str,
    name: Optional[str] = typer.Option(None, help="New project name."),
    color: Optional[str] = typer.Option(None, help="New project color"),
):
    """Update a project."""
    output(
        fmt=config.format,
        model=Project,
        objs=engine.project_update(
            project_id=project_id, name=name, color=color
        ),
    )


@app.command()
@error_handler
def delete(project_id: str):
    """Delete a project."""
    engine.project_delete(project_id=project_id)
