from typing import Optional

import typer

from tracker.output import output
from tracker.models import db, RGB, Project
from tracker.engine import engine

app = typer.Typer(name="project", help="Project commands.")


@app.command()
def list():
    """List all projects."""
    with db.session() as session:
        output(model=Project, objs=engine.project_list(session=session))


@app.command()
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
def delete(name: str):
    """Delete a project."""
    with db.session() as session:
        project = engine.project_get(session=session, name=name)
        if project is None:
            typer.secho(f"Project `{name}` not found.", fg=typer.colors.RED)
            return
        engine.project_delete(session=session, project=project)
