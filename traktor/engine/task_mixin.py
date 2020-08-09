from typing import List, Optional

from sqlalchemy import orm

from traktor import errors
from traktor.models import DB, RGB, Task
from traktor.engine.project_mixin import ProjectMixin


class TaskMixin(ProjectMixin):
    @classmethod
    def task_list(cls, session: orm.Session, project: str) -> List[Task]:
        """List all tasks in a project.

        Args:
            session (orm.Session): SQLAlchemy session.
            project (str): Project name.
        """
        project = cls.project_get(session=session, name=project)

        return DB.filter(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id],
        )

    @classmethod
    def task_get(cls, session: orm.Session, project: str, name: str) -> Task:
        project = cls.project_get(session=session, name=project)
        return DB.get(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id, Task.name == name],
        )

    @classmethod
    def task_get_default(
        cls, session: orm.Session, project: str
    ) -> Optional[Task]:
        project = cls.project_get(session=session, name=project)
        return DB.first(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id, Task.default.is_(True)],
        )

    @staticmethod
    def __set_default_task(session: orm.Session, task: Task, default: bool):
        if default:
            # If the default value for a new task or task update is set to
            # `True` we must first find the previous default task and set it
            # default to `False`.
            old_default = DB.first(
                session=session,
                model=Task,
                filters=[
                    Task.project_id == task.project_id,
                    Task.default.is_(True),
                ],
            )
            if old_default is not None:
                old_default.default = False
                DB.save(session=session, obj=old_default)

            # Now set the new task to be default
            task.default = True
            DB.save(session=session, obj=task)
        else:
            # It's just a non default task
            task.default = False
            DB.save(session=session, obj=task)

    @classmethod
    def task_get_or_create(
        cls,
        session: orm.Session,
        project: str,
        name: str,
        color: Optional[RGB] = None,
        default: Optional[bool] = None,
    ) -> Task:
        project = cls.project_get(session=session, name=project)
        try:
            task = cls.task_get(
                session=session, project=project.name, name=name
            )
            if color is not None:
                if Task.color != color:
                    task.color = color
                    DB.save(session=session, obj=task)

        except errors.ObjectNotFound:
            task = Task(
                project_id=project.id,
                name=name,
                color_hex=(color or RGB()).hex,
            )
            DB.save(session=session, obj=task)

        if default is not None:
            cls.__set_default_task(session=session, task=task, default=default)

        return task

    @classmethod
    def task_update(
        cls,
        session: orm.Session,
        project: str,
        task: str,
        name: Optional[str],
        color: Optional[RGB],
        default: Optional[bool],
    ) -> Task:
        task = cls.task_get(session=session, project=project, name=task)
        # Change name
        if name is not None:
            task.name = name
        # Change color
        if color is not None:
            task.color = color
        # Change default
        if default is not None:
            cls.__set_default_task(
                session=session, task=task, default=default,
            )
        DB.save(session, obj=task)
        return task

    @staticmethod
    def task_delete(session: orm.Session, task: Task):
        DB.delete(session=session, obj=task)
