from typing import Optional

import typer

from traktor.output import output
from traktor.models import RGB, Tag
from traktor.db.sync_db import sync_db as db
from traktor.decorators import error_handler
from traktor.engine import sync_engine as engine


app = typer.Typer(name="tag", help="Tag commands.")


# Make sure that the database exists and it's migrated to the latest version
app.callback()(engine.ensure_db)


@app.command()
@error_handler
def list():
    """List all tags."""
    with db.session() as session:
        output(model=Tag, objs=engine.tag_list(session=session))


@app.command()
@error_handler
def add(name: str, color: Optional[str] = None):
    """Create a tag."""
    if color is not None:
        color = RGB(color)

    with db.session() as session:
        output(
            model=Tag,
            objs=engine.tag_create(session=session, name=name, color=color),
        )


@app.command()
@error_handler
def update(
    tag_id: str,
    name: Optional[str] = typer.Option(None, help="New tag name."),
    color: Optional[str] = typer.Option(None, help="New tag color"),
):
    """Update a project."""
    if color is not None:
        color = RGB(color)

    with db.session() as session:
        output(
            model=Tag,
            objs=engine.tag_update(
                session=session, tag_id=tag_id, name=name, color=color
            ),
        )


@app.command()
@error_handler
def delete(tag_id: str):
    """Delete a tag."""
    with db.session() as session:
        engine.tag_delete(session=session, tag_id=tag_id)
