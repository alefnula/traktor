from typing import Optional

import typer

from tracker.output import output
from tracker.engine import engine
from tracker.models import db, RGB, Task
from tracker.decorators import error_handler


app = typer.Typer(name="task", help="Task commands.")


@app.command()
@error_handler
def list(project: str):
    """List all tasks."""
    with db.session() as session:
        output(
            model=Task, objs=engine.task_list(session=session, project=project)
        )


@app.command()
@error_handler
def create(project: str, name: str, color: Optional[str] = None):
    """Create a task."""
    if color is not None:
        color = RGB.parse(color)

    with db.session() as session:
        output(
            model=Task,
            objs=engine.task_get_or_create(
                session=session, project=project, name=name, color=color
            ),
        )


@app.command()
@error_handler
def rename(project: str, name: str, new_name: str):
    """Rename a task."""
    with db.session() as session:
        output(
            model=Task,
            objs=engine.task_rename(
                session=session, project=project, name=name, new_name=new_name
            ),
        )


@app.command()
@error_handler
def delete(project: str, name: str):
    """Delete a task."""
    with db.session() as session:
        task = engine.task_get(session=session, project=project, name=name)
        engine.task_delete(session=session, task=task)
