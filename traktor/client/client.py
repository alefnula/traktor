from typing import Optional

from traktor.client.http import HttpClient
from traktor.serializers import (
    ProjectCreateSerializer,
    ProjectUpdateSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)


class Client:
    def __init__(self, url):
        self.url = url
        self.http = HttpClient(url=self.url)

    # Projects

    def project_list(self):
        return self.http.get("/projects/")

    def project_get(self, project_id: str):
        return self.http.get(f"/projects/{project_id}/")

    def project_create(self, name: str, color: str = "#000000"):
        serializer = ProjectCreateSerializer(
            data={"name": name, "color": color}
        )
        if serializer.is_valid():
            return self.http.post("/projects/", data=serializer.data)
        return {"errors": serializer.errors}

    def project_update(
        self,
        project_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ):
        serializer = ProjectUpdateSerializer(
            data={"name": name, "color": color}
        )
        if serializer.is_valid():
            return self.http.patch(
                f"/projects/{project_id}/", data=serializer.data
            )
        return {"errors": serializer.errors}

    def project_delete(self, project_id: str):
        return self.http.delete(f"/projects/{project_id}/")

    # Tasks

    def task_list(self, project_id: str):
        return self.http.get(f"/projects/{project_id}/tasks/")

    def task_get(self, project_id: str, task_id: str):
        return self.http.get(f"/projects/{project_id}/tasks/{task_id}/")

    def task_create(
        self, project_id: str, name: str, color: str = "#000000", default=False
    ):
        serializer = TaskCreateSerializer(
            data={"name": name, "color": color, "default": default}
        )
        if serializer.is_valid():
            return self.http.post(
                f"/projects/{project_id}/tasks/", data=serializer.data
            )
        return {"errors": serializer.errors}

    def task_update(
        self,
        project_id: str,
        task_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        default: Optional[bool] = None,
    ):
        serializer = TaskUpdateSerializer(
            data={"name": name, "color": color, "default": default}
        )
        if serializer.is_valid():
            return self.http.patch(
                f"/projects/{project_id}/tasks/{task_id}", data=serializer.data
            )
        return {"errors": serializer.errors}

    def task_delete(self, project_id: str, task_id: str):
        return self.http.delete(f"/projects/{project_id}/tasks/{task_id}")

    # Timer

    def timer_start(self, project_id: str, task_id: Optional[str] = None):
        if task_id is None:
            return self.http.post(f"/timer/start/{project_id}/")
        else:
            return self.http.post(f"/timer/start/{project_id}/{task_id}/")

    def timer_stop(self):
        return self.http.post("/timer/stop/")

    def timer_status(self):
        return self.http.get("/timer/status/")

    def timer_today(self):
        return self.http.get("/timer/today/")

    def timer_report(self, days: int = 0):
        return self.http.get("/timer/report/", params={days: days})
