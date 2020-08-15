from typing import List, Optional

import slugify
from sqlalchemy import orm

from traktor import errors
from traktor.models import RGB, Task
from traktor.db.sync_db import sync_db as db
from traktor.engine.sync_engine.project_mixin import ProjectMixin


class TaskMixin(ProjectMixin):
    @classmethod
    def task_list(
        cls, session: orm.Session, project_id: Optional[str]
    ) -> List[Task]:
        """List all tasks in a project.

        Args:
            session (orm.Session): SQLAlchemy session.
            project_id (str): Project slug.
        """
        if project_id is None:
            return db.all(session=session, model=Task)

        project = cls.project_get(session=session, project_id=project_id)
        return db.filter(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id],
        )

    @classmethod
    def task_get(
        cls, session: orm.Session, project_id: str, task_id: str
    ) -> Task:
        project = cls.project_get(session=session, project_id=project_id)
        return db.get(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id, Task.slug == task_id],
        )

    @classmethod
    def task_get_default(
        cls, session: orm.Session, project_id: str
    ) -> Optional[Task]:
        project = cls.project_get(session=session, project_id=project_id)
        return db.first(
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
            old_default = db.first(
                session=session,
                model=Task,
                filters=[
                    Task.project_id == task.project_id,
                    Task.default.is_(True),
                ],
            )
            if old_default is not None:
                old_default.default = False
                db.save(session=session, obj=old_default)

            # Now set the new task to be default
            task.default = True
            db.save(session=session, obj=task)
        else:
            # It's just a non default task
            task.default = False
            db.save(session=session, obj=task)

    @classmethod
    def task_create(
        cls,
        session: orm.Session,
        project_id: str,
        name: str,
        color: Optional[RGB] = None,
        default: Optional[bool] = None,
    ) -> Task:
        project = cls.project_get(session=session, project_id=project_id)
        try:
            cls.task_get(
                session=session,
                project_id=project.slug,
                task_id=slugify.slugify(name),
            )
            raise errors.ObjectAlreadyExists(
                Task, query={"project_id": project.slug, "name": name}
            )
        except errors.ObjectNotFound:
            task = Task(
                project_id=project.id, name=name, color=(color or RGB()).hex,
            )
            db.save(session=session, obj=task)

        if default is not None:
            cls.__set_default_task(session=session, task=task, default=default)

        return task

    @classmethod
    def task_update(
        cls,
        session: orm.Session,
        project_id: str,
        task_id: str,
        name: Optional[str],
        color: Optional[RGB],
        default: Optional[bool],
    ) -> Task:
        task = cls.task_get(
            session=session, project_id=project_id, task_id=task_id
        )
        # Change name
        if name is not None:
            task.rename(name)
        # Change color
        if color is not None:
            task.color = color
        # Change default
        if default is not None:
            cls.__set_default_task(
                session=session, task=task, default=default,
            )
        db.save(session, obj=task)
        return task

    @classmethod
    def task_delete(cls, session: orm.Session, project_id: str, task_id: str):
        project = cls.project_get(session=session, project_id=project_id)
        task = cls.task_get(
            session=session, project_id=project.slug, task_id=task_id
        )
        db.delete(session=session, obj=task)
