from typing import List, Optional

from django_tea import errors

from traktor.models import Project, Task
from traktor.engine.project_mixin import ProjectMixin


class TaskMixin(ProjectMixin):
    @classmethod
    def task_list(cls, project_id: Optional[str]) -> List[Task]:
        """List all tasks in a project.

        Args:
            project_id (str): Project slug.
        """
        if project_id is None:
            query = Task.objects.all()
        else:
            query = Task.objects.filter(project__slug=project_id)

        return list(query)

    @classmethod
    def task_get(cls, project_id: str, task_id: str) -> Task:
        try:
            return Task.get_by_slug(slug=task_id, project__slug=project_id)
        except Task.DoesNotExist:
            raise errors.ObjectNotFound(
                model=Task,
                query={"project_id": project_id, "task_id": task_id},
            )

    @classmethod
    def task_get_default(cls, project_id: str) -> Optional[Task]:
        try:
            return Task.objects.get(project__slug=project_id, default=True)
        except Task.DoesNotExist:
            raise errors.ObjectNotFound(
                model=Task, query={"project_id": project_id, "default": True}
            )

    @staticmethod
    def __set_default_task(task: Task, default: bool):
        if default:
            # If the default value for a new task or task update is set to
            # `True` we must first find the previous default task and set it
            # default to `False`.
            try:
                old_default = Task.objects.get(
                    project=task.project, default=True
                )
                # If it's not the same task
                if old_default.pk != task.pk:
                    old_default.default = False
                    old_default.save()
            except Task.DoesNotExist:
                # All OK!
                pass

            # Now set the new task to be default
            task.default = True
            task.save()
        else:
            # It's just a non default task
            task.default = False
            task.save()

    @classmethod
    def task_create(
        cls,
        project_id: str,
        name: str,
        color: Optional[str] = None,
        default: Optional[bool] = None,
    ) -> Task:
        project = Project.get_by_slug(slug=project_id)
        try:
            Task.get_by_slug_field(value=name, project__slug=project_id)
            raise errors.ObjectAlreadyExists(
                Task, query={"project_id": project.slug, "name": name}
            )
        except Task.DoesNotExist:
            task = Task.objects.create(
                project=project,
                name=name,
                color=color or Task.color.field.default,
            )
            task.save()

        if default is not None:
            cls.__set_default_task(task=task, default=default)

        return task

    @classmethod
    def task_update(
        cls,
        project_id: str,
        task_id: str,
        name: Optional[str],
        color: Optional[str],
        default: Optional[bool],
    ) -> Task:
        task = cls.task_get(project_id=project_id, task_id=task_id)
        # Change name
        if name is not None:
            task.name = name
        # Change color
        if color is not None:
            task.color = color
        # Change default
        if default is not None:
            cls.__set_default_task(task=task, default=default)
        task.save()
        return task

    @classmethod
    def task_delete(cls, project_id: str, task_id: str):
        task = cls.task_get(project_id=project_id, task_id=task_id)
        task.delete()
