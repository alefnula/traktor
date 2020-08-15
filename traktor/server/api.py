from fastapi import FastAPI

from traktor import errors
from traktor.engine.async_engine import async_engine
from traktor.server.response import tjson, JSONResponse
from traktor.models import ProjectCreateRequest, ProjectUpdateRequest
from traktor.server.exception_handler import traktor_exception_handler

app = FastAPI()
app.exception_handler(errors.TraktorError)(traktor_exception_handler)

# Project


@app.get("/projects/")
@tjson
async def project_list():
    """List all projects."""
    return await async_engine.project_list()


@app.post("/projects/")
@tjson
async def project_add(project: ProjectCreateRequest):
    return await async_engine.project_create(project_request=project)


@app.get("/projects/{project_id}/")
@tjson
async def project_get(project_id: str):
    return await async_engine.project_get(project_id=project_id)


@app.patch("/projects/{project_id}/")
@tjson
async def project_update(project_id: str, project: ProjectUpdateRequest):
    return await async_engine.project_update(
        project_id=project_id, request=project
    )


@app.delete("/projects/{project_id}/")
async def project_delete(project_id: str):
    if await async_engine.project_delete(project_id=project_id):
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
    return await async_engine.task_list(project_id=project_id)


@app.get("/projects/{project_id}/tasks/{task_id}/")
@tjson
async def task_get(project_id: str, task_id: str):
    return await async_engine.task_get(project_id=project_id, task_id=task_id)


@app.delete("/projects/{project_id}/tasks/{task_id}/")
async def task_delete(project_id: str, task_id: str):
    if await async_engine.task_delete(project_id=project_id, task_id=task_id):
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
    return await async_engine.tag_list()


@app.get("/tags/{tag_id}/")
@tjson
async def tag_get(tag_id: str):
    return await async_engine.tag_get(tag_id=tag_id)


@app.delete("/tag/{tag_id}/")
async def tag_delete(tag_id: str):
    if await async_engine.tag_delete(tag_id=tag_id):
        return JSONResponse(status_code=204, content={"detail": "OK"})
    else:
        return JSONResponse(
            status_code=500, content={"detail": "Tag could not be deleted."},
        )
