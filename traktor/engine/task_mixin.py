from typing import List, Optional

from tea_django import errors

from traktor.models import User, Project, Task
from traktor.engine.project_mixin import ProjectMixin


class TaskMixin(ProjectMixin):
    @classmethod
    def task_list(cls, user: User, project_id: Optional[str]) -> List[Task]:
        """List all tasks in a project.

        Args:
            user (User): Selected user.
            project_id (str): Project slug.
        """
        if project_id is None:
            query = Task.objects.filter(project__user=user)
        else:
            query = Task.objects.filter(
                project__user=user, project__slug=project_id
            )

        return list(query)

    @classmethod
    def task_get(cls, user: User, project_id: str, task_id: str) -> Task:
        """Get a specific task.

        Args:
            user (User): Selected user.
            project_id (str): Project slug.
            task_id (str): Task slug.
        """
        try:
            return Task.get_by_slug(
                slug=task_id, project__user=user, project__slug=project_id,
            )
        except Task.DoesNotExist:
            raise errors.ObjectNotFound(
                model=Task,
                query={
                    "user": user.username,
                    "project_id": project_id,
                    "task_id": task_id,
                },
            )

    @classmethod
    def task_get_default(cls, user: User, project_id: str) -> Optional[Task]:
        """Get default task for a project.

        Args:
            user (User): Selected user.
            project_id (str): Project slug.
        """
        try:
            return Task.objects.get(
                project__user=user, project__slug=project_id, default=True
            )
        except Task.DoesNotExist:
            raise errors.ObjectNotFound(
                model=Task,
                query={
                    "user": user.username,
                    "project_id": project_id,
                    "default": True,
                },
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
        user: User,
        project_id: str,
        name: str,
        color: Optional[str] = None,
        default: Optional[bool] = None,
    ) -> Task:
        """Create a task.

        Args:
            user (User): Selected user.
            project_id (str): Project slug.
            name (str): Task name.
            color (str, optional): Task color.
            default (bool, optional): Is this a default task for this project.
        """
        project = Project.get_by_slug(slug=project_id, user=user)
        try:
            Task.get_by_slug_field(value=name, project__id=project.id)
            raise errors.ObjectAlreadyExists(
                Task,
                query={
                    "user": user.username,
                    "project_id": project.slug,
                    "name": name,
                },
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
        user: User,
        project_id: str,
        task_id: str,
        name: Optional[str],
        color: Optional[str],
        default: Optional[bool],
    ) -> Task:
        """Update a task.

        Args:
            user (User): Selected user.
            project_id (str): Project slug.
            task_id (str): Task slug.
            name (str, optional): Task name.
            color (str, optional): Task color.
            default (bool, optional): Is this a default task for this project.
        """
        task = cls.task_get(user=user, project_id=project_id, task_id=task_id)
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
    def task_delete(cls, user: User, project_id: str, task_id: str):
        """Delete a task.

        Args:
            user (User): Selected user.
            project_id (str): Project slug.
            task_id (str): Task slug.
        """
        task = cls.task_get(user=user, project_id=project_id, task_id=task_id)
        task.delete()
