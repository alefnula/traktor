from typing import List, Optional


from traktor import errors
from traktor.db.async_db import async_db as db
from traktor.engine.async_engine.project_mixin import ProjectMixin
from traktor.models import RGB, Task, TaskCreateRequest, TaskUpdateRequest


class TaskMixin(ProjectMixin):
    @classmethod
    async def task_list(cls, project_id: str) -> List[Task]:
        """List all tasks in a project.

        Args:
            project_id (str): Project id or project slug.
        """
        project = await cls.project_get(project_id=project_id)
        return await db.filter(
            model=Task, filters=[Task.project_id == project.id]
        )

    @classmethod
    async def task_get(cls, project_id: str, task_id: str) -> Task:
        project = await cls.project_get(project_id=project_id)
        return await db.get(
            model=Task,
            filters=[Task.project_id == project.id, Task.slug == task_id],
        )

    @staticmethod
    async def task_get_by_uuid(task_id: str) -> Task:
        return await db.get_by_id(model=Task, obj_id=task_id)

    @classmethod
    async def task_get_default(cls, project_id: str) -> Optional[Task]:
        project = await cls.project_get(project_id=project_id)
        return await db.first(
            model=Task,
            filters=[Task.project_id == project.id, Task.default.is_(True)],
        )

    @staticmethod
    async def __set_default_task(task: Task, default: bool):
        if default:
            # If the default value for a new task or task update is set to
            # `True` we must first find the previous default task and set it
            # default to `False`.
            old_default = await db.first(
                model=Task,
                filters=[
                    Task.project_id == task.project_id,
                    Task.default.is_(True),
                ],
            )
            if old_default is not None:
                old_default.default = False
                await db.save(old_default)

            # Now set the new task to be default
            task.default = True
            db.save(obj=task)
        else:
            # It's just a non default task
            task.default = False
            db.save(obj=task)

    @classmethod
    async def task_create(
        cls, project_id: str, request: TaskCreateRequest
    ) -> Task:
        try:
            await cls.task_get(project_id=project_id, task_id=request.slug)

            raise errors.ObjectAlreadyExists(
                model=Task,
                query={"project_id": project_id, "name": request.name},
            )
        except errors.ObjectNotFound:
            project = await cls.project_get(project_id=project_id)
            task = Task.create(
                project_id=project.id,
                name=request.name,
                color=(request.color or RGB().hex),
            )
            await cls.__set_default_task(task, default=request.default)
            return await db.save(task)

    @classmethod
    async def task_update(
        cls, project_id: str, task_id: str, request: TaskUpdateRequest,
    ) -> Task:
        task = await cls.task_get(project_id=project_id, task_id=task_id)
        # Change name
        if request.name is not None:
            task.rename(request.name)
        # Change color
        if request.color is not None:
            task.color = request.color
        if request.default is not None:
            await cls.__set_default_task(task, default=request.default)
        return await db.update(task)

    @classmethod
    async def task_delete(cls, project_id: str, task_id: str) -> bool:
        task = await cls.task_get(project_id=project_id, task_id=task_id)
        return await db.delete(obj=task)
