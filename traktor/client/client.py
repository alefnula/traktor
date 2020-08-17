from typing import Optional

from traktor.client import models
from traktor.client.http import HttpClient


class Client:
    def __init__(self, url):
        self.url = url
        self.http = HttpClient(url=self.url)

    # Projects

    async def project_list(self):
        return await self.http.get("/projects/")

    async def project_create(self, request: models.ProjectCreateRequest):
        return await self.http.post("/projects/", data=request.dict())

    async def project_get(self, project_id: str):
        return await self.http.get(f"/projects/{project_id}/")

    async def project_update(
        self, project_id: str, request: models.ProjectUpdateRequest
    ):
        return await self.http.patch(
            f"/projects/{project_id}", data=request.dict()
        )

    async def project_delete(self, project_id: str):
        return await self.http.delete(f"/projects/{project_id}/")

    # Tasks

    async def task_list(self, project_id: str):
        return await self.http.get(f"/projects/{project_id}/tasks/")

    async def task_create(
        self, project_id: str, request: models.TaskCreateRequest
    ):
        return await self.http.post(
            f"/projects/{project_id}/tasks/", data=request.dict()
        )

    async def task_get(self, project_id: str, task_id: str):
        return await self.http.get(f"/projects/{project_id}/tasks/{task_id}/")

    async def task_update(
        self, project_id: str, task_id: str, request: models.TaskUpdateRequest
    ):
        return await self.http.patch(
            f"/projects/{project_id}/tasks/{task_id}", data=request.dict()
        )

    async def task_delete(self, project_id: str, task_id: str):
        return await self.http.delete(
            f"/projects/{project_id}/tasks/{task_id}"
        )

    # Timer

    async def timer_start(
        self, project_id: str, task_id: Optional[str] = None
    ):
        if task_id is None:
            return await self.http.post(f"/timer/start/{project_id}/")
        else:
            return await self.http.post(
                f"/timer/start/{project_id}/{task_id}/"
            )

    async def timer_stop(self):
        return await self.http.post("/timer/stop/")

    async def timer_status(self):
        return await self.http.get("/timer/status/")

    async def timer_today(self):
        return await self.http.get("/timer/today/")

    async def timer_report(self, days: int = 0):
        return await self.http.get("/timer/report/", params={days: days})
