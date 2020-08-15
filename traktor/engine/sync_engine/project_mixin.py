from typing import List, Optional

import slugify
from sqlalchemy import orm

from traktor import errors
from traktor.models import RGB, Project
from traktor.db.sync_db import sync_db as db


class ProjectMixin:
    @staticmethod
    def project_list(session: orm.Session) -> List[Project]:
        return db.all(session=session, model=Project)

    @staticmethod
    def project_get(session: orm.Session, project_id: str) -> Project:
        return db.get(
            session=session,
            model=Project,
            filters=[Project.slug == project_id],
        )

    @classmethod
    def project_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None
    ) -> Project:
        try:
            cls.project_get(session=session, project_id=slugify.slugify(name))
            raise errors.ObjectAlreadyExists(
                model=Project, query={"name": name}
            )
        except errors.ObjectNotFound:
            project = Project(name=name, color=(color or RGB()).hex)
            db.save(session=session, obj=project)

        return project

    @classmethod
    def project_update(
        cls,
        session: orm.Session,
        project_id: str,
        name: Optional[str],
        color: Optional[RGB],
    ) -> Project:
        project = cls.project_get(session=session, project_id=project_id)
        # Change name
        if name is not None:
            project.rename(name=name)
        # Change color
        if color is not None:
            project.color = color
        db.save(session, obj=project)
        return project

    @classmethod
    def project_delete(cls, session: orm.Session, project_id: str):
        project = cls.project_get(session=session, project_id=project_id)
        db.delete(session=session, obj=project)
