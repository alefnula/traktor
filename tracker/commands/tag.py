from typing import Optional

import typer

from tracker.output import output
from tracker.engine import engine
from tracker.models import db, RGB, Tag
from tracker.decorators import error_handler


app = typer.Typer(name="tag", help="Tag commands.")


@app.command()
@error_handler
def list():
    """List all tags."""
    with db.session() as session:
        output(model=Tag, objs=engine.tag_list(session=session))


@app.command()
@error_handler
def create(name: str, color: Optional[str] = None):
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
