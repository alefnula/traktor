import asyncio
import functools
from typing import Optional

import typer
from rich import print

from traktor.config import config
from traktor.client import Client
from traktor.client import models


app = typer.Typer(name="client", help="HTTP client operations.", hidden=True)

client = Client(url=config.url)


def aio(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        corrutine = func(*args, **kwargs)
        print(asyncio.run(corrutine))

    return wrapper


# Projects


@app.command()
@aio
def project_list():
    return client.project_list()


@app.command()
@aio
def project_get(project_id: str):
    return client.project_get(project_id=project_id)


@app.command()
@aio
def project_create(name: str, color: Optional[str] = models.RGB().hex):
    return client.project_create(
        request=models.ProjectCreateRequest(name=name, color=color)
    )


@app.command()
@aio
def project_update(
    project_id: str, name: Optional[str] = None, color: Optional[str] = None
):
    return client.project_update(
        project_id=project_id,
        request=models.ProjectUpdateRequest(name=name, color=color),
    )


@app.command()
@aio
def project_delete(project_id: str):
    return client.project_delete(project_id=project_id)


# Tasks


@app.command()
@aio
def task_list(project_id: str):
    return client.task_list(project_id=project_id)


@app.command()
@aio
def task_get(project_id: str, task_id: str):
    return client.task_get(project_id=project_id, task_id=task_id)


@app.command()
@aio
def task_create(
    project_id: str,
    name: str,
    color: Optional[str] = models.RGB().hex,
    default: bool = False,
):
    return client.task_create(
        project_id=project_id,
        request=models.TaskCreateRequest(
            name=name, color=color, default=default
        ),
    )


@app.command()
@aio
def task_update(
    project_id: str,
    task_id: str,
    name: Optional[str] = None,
    color: Optional[str] = None,
    default: Optional[bool] = None,
):
    return client.task_update(
        project_id=project_id,
        task_id=task_id,
        request=models.TaskUpdateRequest(
            name=name, color=color, default=default
        ),
    )


@app.command()
@aio
def task_delete(project_id: str, task_id: str):
    return client.task_delete(project_id=project_id, task_id=task_id)


# Tags


@app.command()
@aio
def tag_list():
    return client.tag_list()


@app.command()
@aio
def tag_get(tag_id: str):
    return client.tag_get(tag_id=tag_id)


@app.command()
@aio
def tag_create(name: str, color: Optional[str] = models.RGB().hex):
    return client.tag_create(models.TagCreateRequest(name=name, color=color))


@app.command()
@aio
def tag_update(
    tag_id: str, name: Optional[str] = None, color: Optional[str] = None
):
    return client.tag_update(
        tag_id=tag_id, request=models.TagUpdateRequest(name=name, color=color)
    )


@app.command()
@aio
def tag_delete(tag_id: str):
    return client.tag_delete(tag_id=tag_id)


# Timer


@app.command()
@aio
def timer_start(project_id: str, task_id: Optional[str] = None):
    return client.timer_start(project_id=project_id, task_id=task_id)


@app.command()
@aio
def timer_stop():
    return client.timer_stop()


@app.command()
@aio
def timer_status():
    return client.timer_status()


@app.command()
@aio
def timer_today():
    return client.timer_today()


@app.command()
@aio
def timer_report(days: int = 0):
    return client.timer_report(days=days)
