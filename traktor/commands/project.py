from typing import Optional

import typer

from traktor.output import output
from traktor.models import RGB, Project
from traktor.db.sync_db import sync_db as db
from traktor.decorators import error_handler
from traktor.engine import sync_engine as engine


app = typer.Typer(name="project", help="Project commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.ensure_db)


@app.command()
@error_handler
def list():
    """List all projects."""
    with db.session() as session:
        output(model=Project, objs=engine.project_list(session=session))


@app.command()
@error_handler
def add(name: str, color: Optional[str] = None):
    """Create a project."""
    if color is not None:
        color = RGB(color)

    with db.session() as session:
        output(
            model=Project,
            objs=engine.project_create(
                session=session, name=name, color=color
            ),
        )


@app.command()
@error_handler
def update(
    project_id: str,
    name: Optional[str] = typer.Option(None, help="New project name."),
    color: Optional[str] = typer.Option(None, help="New project color"),
):
    """Update a project."""
    if color is not None:
        color = RGB(color)

    with db.session() as session:
        output(
            model=Project,
            objs=engine.project_update(
                session=session, project_id=project_id, name=name, color=color
            ),
        )


@app.command()
@error_handler
def delete(project_id: str):
    """Delete a project."""
    with db.session() as session:
        engine.project_delete(session=session, project_id=project_id)
