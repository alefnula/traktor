from typing import Optional

import typer

from traktor.output import output
from traktor.engine import engine
from traktor.models import db, RGB, Project
from traktor.decorators import error_handler


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
        color = RGB.parse(color)

    with db.session() as session:
        output(
            model=Project,
            objs=engine.project_get_or_create(
                session=session, name=name, color=color
            ),
        )


@app.command()
@error_handler
def update(
    project: str,
    name: Optional[str] = typer.Option(None, help="New project name."),
    color: Optional[str] = typer.Option(None, help="New project color"),
):
    """Update a project."""
    if color is not None:
        color = RGB.parse(color)

    with db.session() as session:
        output(
            model=Project,
            objs=engine.project_update(
                session=session, project=project, name=name, color=color
            ),
        )


@app.command()
@error_handler
def delete(name: str):
    """Delete a project."""
    with db.session() as session:
        project = engine.project_get(session=session, name=name)
        engine.project_delete(session=session, project=project)
