from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView


from traktor import serializers
from traktor.engine import engine


# Project


class ProjectListCreate(APIView):
    def get(self, request: Request):
        """List all projects."""
        return Response(
            serializers.ProjectSerializer(
                engine.project_list(), many=True
            ).data
        )

    def post(self, request: Request):
        """Create a project."""
        pass


class ProjectGetUpdateDelete(APIView):
    def get(self, request: Request, project_id: str):
        """Get a project."""
        return Response(
            serializers.ProjectSerializer(
                engine.project_get(project_id=project_id)
            ).data
        )

    def patch(self, request: Request, project_id: str):
        """Update a project."""
        pass

    def delete(self, request: Request, project_id: str):
        """Delete a project."""
        if engine.project_delete(project_id=project_id):
            return Response(status=204, data={"detail": "OK"})
        else:
            return Response(
                status=500, data={"error": "Project could not be deleted."}
            )


# Task


class TaskListCreate(APIView):
    def get(self, request: Request, project_id: str):
        """List all tasks in project.."""
        return Response(
            serializers.TaskSerializer(
                engine.task_list(project_id=project_id), many=True
            ).data
        )

    def post(self, request: Request, project_id: str):
        """Create a task.."""
        pass


class TaskGetUpdateDelete(APIView):
    def get(self, request: Request, project_id: str, task_id: str):
        """Get task details."""
        return Response(
            serializers.TaskSerializer(
                engine.task_get(project_id=project_id, task_id=task_id)
            ).data
        )

    def patch(self, request: Request, project_id: str, task_id: str):
        """Update a task."""
        pass

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
def timer_default_start(requests: Request, project_id: str):
    return Response(
        serializers.EntrySerializer(
            engine.timer_start(project_id=project_id)
        ).data
    )


@api_view(["POST"])
def timer_start(request: Request, project_id: str, task_id: str):
    return Response(
        serializers.EntrySerializer(
            engine.timer_start(project_id=project_id, task_id=task_id)
        ).data
    )


@api_view(["POST"])
def timer_stop(request: Request):
    return Response(serializers.EntrySerializer(engine.timer_stop()).data)


@api_view(["GET"])
def timer_status(request: Request):
    return Response(serializers.EntrySerializer(engine.timer_status()).data)


@api_view(["GET"])
def timer_today(request: Request):
    return Response(
        serializers.ReportSerializer(engine.timer_today(), many=True).data
    )


@api_view(["GET"])
def timer_report(request: Request):
    days = request.query_params.get("days", 0)
    return Response(
        serializers.ReportSerializer(
            engine.timer_report(days=days), many=True
        ).data
    )
