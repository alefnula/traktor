from uuid import UUID
from typing import List, Optional


from traktor.models import Task
from traktor.db.async_db import async_db as db
from traktor.engine.async_engine.project_mixin import ProjectMixin


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
        try:
            UUID(task_id)
            return await db.get_by_id(model=Task, obj_id=task_id)
        except ValueError:
            project = await cls.project_get(project_id=project_id)
            return await db.get(
                model=Task,
                filters=[Task.project_id == project.id, Task.name == task_id],
            )

    async def task_get_default(cls, project_id: str) -> Optional[Task]:
        project = await cls.project_get(project_id=project_id)
        return await db.first(
            model=Task,
            filters=[Task.project_id == project.id, Task.default.is_(True)],
        )

    @classmethod
    async def task_delete(cls, project_id: str, task_id: str) -> bool:
        task = await cls.task_get(project_id=project_id, task_id=task_id)
        return await db.delete(obj=task)
