from typing import Optional

import typer

from traktor.output import output
from traktor.models import RGB, Task
from traktor.db.sync_db import sync_db as db
from traktor.decorators import error_handler
from traktor.engine import sync_engine as engine


app = typer.Typer(name="task", help="Task commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.ensure_db)


@app.command()
@error_handler
def list(project_id: Optional[str] = typer.Argument(None)):
    """List all tasks."""
    with db.session() as session:
        output(
            model=Task,
            objs=engine.task_list(session=session, project_id=project_id),
        )


@app.command()
@error_handler
def add(
    project_id: str,
    name: str,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    """Create a task."""
    if color is not None:
        color = RGB(color)

    with db.session() as session:
        output(
            model=Task,
            objs=engine.task_create(
                session=session,
                project_id=project_id,
                name=name,
                color=color,
                default=default,
            ),
        )


@app.command()
@error_handler
def update(
    project_id: str,
    task_id: str,
    name: Optional[str] = typer.Option(None, help="New task name."),
    color: Optional[str] = typer.Option(None, help="New task color"),
    default: Optional[bool] = typer.Option(
        None, help="Is this a default task."
    ),
):
    """Update a project."""
    if color is not None:
        color = RGB(color)

    with db.session() as session:
        output(
            model=Task,
            objs=engine.task_update(
                session=session,
                project_id=project_id,
                task_id=task_id,
                name=name,
                color=color,
                default=default,
            ),
        )


@app.command()
@error_handler
def delete(project_id: str, task_id: str):
    """Delete a task."""
    with db.session() as session:
        engine.task_delete(
            session=session, project_id=project_id, task_id=task_id
        )
