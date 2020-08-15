import typer
import uvicorn


app = typer.Typer(name="server", help="Web server commands.")


@app.command()
def start(
    host: str = "127.0.0.1",
    port: int = 5000,
    workers: int = 2,
    reload: bool = True,
    log_level: str = "info",
):
    """Run web server."""
    print(reload)
    uvicorn.run(
        "traktor.server:server",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
        log_level=log_level,
    )
