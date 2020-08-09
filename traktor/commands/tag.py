from typing import Optional

import typer

from traktor.output import output
from traktor.engine import engine
from traktor.models import db, RGB, Tag
from traktor.decorators import error_handler


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
        color = RGB.parse(color)

    with db.session() as session:
        output(
            model=Tag,
            objs=engine.tag_get_or_create(
                session=session, name=name, color=color
            ),
        )


@app.command()
@error_handler
def update(
    tag: str,
    name: Optional[str] = typer.Option(None, help="New tag name."),
    color: Optional[str] = typer.Option(None, help="New tag color"),
):
    """Update a project."""
    if color is not None:
        color = RGB.parse(color)

    with db.session() as session:
        output(
            model=Tag,
            objs=engine.tag_update(
                session=session, tag=tag, name=name, color=color
            ),
        )


@app.command()
@error_handler
def rename(name: str, new_name: str):
    """Rename a tag."""
    with db.session() as session:
        output(
            model=Tag,
            objs=engine.tag_rename(
                session=session, name=name, new_name=new_name
            ),
        )


@app.command()
@error_handler
def delete(name: str):
    """Delete a tag."""
    with db.session() as session:
        tag = engine.tag_get(session=session, name=name)
        engine.tag_delete(session=session, tag=tag)
