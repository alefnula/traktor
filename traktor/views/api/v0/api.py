import functools
from typing import Optional, Type

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view, APIView


from traktor.serializers import (
    ProjectSerializer,
    ProjectCreateSerializer,
    ProjectUpdateSerializer,
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    EntrySerializer,
    ReportSerializer,
)
from traktor.engine import engine


# Project


def handler(serializer: Optional[Type[Serializer]] = None, many=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if serializer is None:
                return Response(result)
            else:
                return Response(serializer(result, many=many).data)

        return wrapper

    return decorator


class ProjectListCreate(APIView):
    @handler(ProjectSerializer, many=True)
    def get(self, request: Request):
        """List all projects."""
        return engine.project_list()

    @handler(ProjectSerializer)
    def post(self, request: Request):
        """Create a project."""
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return engine.project_create(**serializer.data)


class ProjectGetUpdateDelete(APIView):
    @handler(ProjectSerializer)
    def get(self, request: Request, project_id: str):
        """Get a project."""
        return engine.project_get(project_id=project_id)

    @handler(ProjectSerializer)
    def patch(self, request: Request, project_id: str):
        """Update a project."""
        project = engine.project_get(project_id=project_id)
        serializer = ProjectUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return engine.project_update(project.id, **serializer.data)

    def delete(self, request: Request, project_id: str):
        """Delete a project."""
        if engine.project_delete(project_id=project_id):
            return Response(status=204, data={"detail": "OK"})
        else:
            return Response(
                status=500, data={"errors": ["Project could not be deleted."]}
            )


# Task


class TaskListCreate(APIView):
    @handler(TaskSerializer, many=True)
    def get(self, request: Request, project_id: str):
        """List all tasks in project.."""
        return engine.task_list(project_id=project_id)

    @handler(TaskSerializer)
    def post(self, request: Request, project_id: str):
        """Create a task.."""
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return engine.task_create(project_id=project_id, **serializer.data)


class TaskGetUpdateDelete(APIView):
    @handler(TaskSerializer)
    def get(self, request: Request, project_id: str, task_id: str):
        """Get task details."""
        return engine.task_get(project_id=project_id, task_id=task_id)

    @handler(TaskSerializer)
    def patch(self, request: Request, project_id: str, task_id: str):
        """Update a task."""
        serializer = TaskUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return engine.task_update(
                project_id=project_id, task_id=task_id, **serializer.data
            )

    def delete(self, request: Request, project_id: str, task_id: str):
        """Delete a task."""
        if engine.task_delete(project_id=project_id, task_id=task_id):
            return Response(status=204, data={"detail": "OK"})
        else:
            return Response(
                status=500, data={"error": "Task could not be deleted."}
            )


# Timer


@api_view(["POST"])
@handler(EntrySerializer)
def timer_default_start(requests: Request, project_id: str):
    return engine.timer_start(project_id=project_id)


@api_view(["POST"])
@handler(EntrySerializer)
def timer_start(request: Request, project_id: str, task_id: str):
    return engine.timer_start(project_id=project_id, task_id=task_id)


@api_view(["POST"])
@handler(EntrySerializer)
def timer_stop(request: Request):
    return engine.timer_stop()


@api_view(["GET"])
@handler(EntrySerializer)
def timer_status(request: Request):
    return engine.timer_status()


@api_view(["GET"])
@handler(ReportSerializer, many=True)
def timer_today(request: Request):
    return engine.timer_today()


@api_view(["GET"])
@handler(ReportSerializer, many=True)
def timer_report(request: Request):
    days = request.query_params.get("days", 0)
    return engine.timer_report(days=days)
