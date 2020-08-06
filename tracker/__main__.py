import typer

from tracker.commands import db

app = typer.Typer()
app.add_typer(db.app)


if __name__ == "__main__":
    app()
