from typing import Optional

import typer

from traktor.output import output
from traktor.engine import engine
from traktor.models import db, RGB, Project
from traktor.decorators import error_handler


app = typer.Typer(name="project", help="Project commands.")


@app.command()
@error_handler
def list():
    """List all projects."""
    with db.session() as session:
        output(model=Project, objs=engine.project_list(session=session))


@app.command()
@error_handler
def create(name: str, color: Optional[str] = None):
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
def rename(name: str, new_name: str):
    """Rename a project."""
    with db.session() as session:
        output(
            model=Project,
            objs=engine.project_rename(
                session=session, name=name, new_name=new_name
            ),
        )


@app.command()
@error_handler
def delete(name: str):
    """Delete a project."""
    with db.session() as session:
        project = engine.project_get(session=session, name=name)
        engine.project_delete(session=session, project=project)
