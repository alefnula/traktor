from fastapi import FastAPI

from traktor import errors
from traktor.engine.async_engine import async_engine as engine
from traktor.server.response import tjson, JSONResponse
from traktor.server.exception_handler import traktor_exception_handler
from traktor.models import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    TaskCreateRequest,
    TaskUpdateRequest,
    TagCreateRequest,
    TagUpdateRequest,
)


app = FastAPI()
app.exception_handler(errors.TraktorError)(traktor_exception_handler)

# Project


@app.get("/projects/")
@tjson
async def project_list():
    """List all projects."""
    return await engine.project_list()


@app.post("/projects/")
@tjson
async def project_create(request: ProjectCreateRequest):
    return await engine.project_create(request=request)


@app.get("/projects/{project_id}/")
@tjson
async def project_get(project_id: str):
    return await engine.project_get(project_id=project_id)


@app.patch("/projects/{project_id}/")
@tjson
async def project_update(project_id: str, request: ProjectUpdateRequest):
    return await engine.project_update(project_id=project_id, request=request)


@app.delete("/projects/{project_id}/")
async def project_delete(project_id: str):
    if await engine.project_delete(project_id=project_id):
        return JSONResponse(status_code=204, content={"detail": "OK"})
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Project could not be deleted."},
        )


# Task


@app.get("/projects/{project_id}/tasks/")
@tjson
async def task_list(project_id: str):
    """List all tasks in a project."""
    return await engine.task_list(project_id=project_id)


@app.post("/projects/{project_id}/tasks/")
@tjson
async def task_create(project_id: str, request: TaskCreateRequest):
    return await engine.task_create(project_id=project_id, request=request)


@app.get("/projects/{project_id}/tasks/{task_id}/")
@tjson
async def task_get(project_id: str, task_id: str):
    return await engine.task_get(project_id=project_id, task_id=task_id)


@app.patch("/projects/{project_id}/tasks/{task_id}/")
@tjson
async def task_update(
    project_id: str, task_id: str, request: TaskUpdateRequest
):
    return await engine.task_update(
        project_id=project_id, task_id=task_id, request=request
    )


@app.delete("/projects/{project_id}/tasks/{task_id}/")
async def task_delete(project_id: str, task_id: str):
    if await engine.task_delete(project_id=project_id, task_id=task_id):
        return JSONResponse(status_code=204, content={"detail": "OK"})
    else:
        return JSONResponse(
            status_code=500, content={"detail": "Task could not be deleted."},
        )


# Tag


@app.get("/tags/")
@tjson
async def tag_list():
    """List all tags."""
    return await engine.tag_list()


@app.post("/tags/")
@tjson
async def tag_add(request: TagCreateRequest):
    return await engine.tag_create(request=request)


@app.get("/tags/{tag_id}/")
@tjson
async def tag_get(tag_id: str):
    return await engine.tag_get(tag_id=tag_id)


@app.patch("/tags/{tag_id}/")
@tjson
async def tag_update(tag_id: str, request: TagUpdateRequest):
    return await engine.tag_update(tag_id=tag_id, request=request)


@app.delete("/tag/{tag_id}/")
async def tag_delete(tag_id: str):
    if await engine.tag_delete(tag_id=tag_id):
        return JSONResponse(status_code=204, content={"detail": "OK"})
    else:
        return JSONResponse(
            status_code=500, content={"detail": "Tag could not be deleted."},
        )


# Timer


@app.post("/timer/start/{project_id}/")
@tjson
async def timer_default_start(project_id: str):
    return await engine.timer_start(project_id=project_id)


@app.post("/timer/start/{project_id}/{task_id}/")
@tjson
async def timer_start(project_id: str, task_id: str):
    return await engine.timer_start(project_id=project_id, task_id=task_id)


@app.post("/timer/stop/")
@tjson
async def timer_stop():
    return await engine.timer_stop()


@app.get("/timer/status/")
@tjson
async def timer_status():
    return await engine.timer_status()


@app.get("/timer/today/")
@tjson
async def timer_today():
    return await engine.timer_today()


@app.get("/timer/report")
@tjson
async def timer_report(days: int = 0):
    return await engine.timer_report(days=days)
