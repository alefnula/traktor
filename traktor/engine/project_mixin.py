from typing import List, Optional


from sqlalchemy import orm

from traktor import errors
from traktor.models import DB, RGB, Project


class ProjectMixin:
    @staticmethod
    def project_list(session: orm.Session) -> List[Project]:
        return DB.all(session=session, model=Project)

    @staticmethod
    def project_get(session: orm.Session, name: str) -> Project:
        return DB.get(
            session=session, model=Project, filters=[Project.name == name]
        )

    @classmethod
    def project_get_or_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None
    ) -> Project:
        try:
            project = cls.project_get(session=session, name=name)
            if color is not None:
                if project.color != color:
                    project.color = color
                    DB.save(session=session, obj=project)
        except errors.ObjectNotFound:
            project = Project(name=name, color_hex=(color or RGB()).hex)
            DB.save(session=session, obj=project)

        return project

    @classmethod
    def project_update(
        cls,
        session: orm.Session,
        project: str,
        name: Optional[str],
        color: Optional[RGB],
    ) -> Project:
        project = cls.project_get(session=session, name=project)
        # Change name
        if name is not None:
            project.name = name
        # Change color
        if color is not None:
            project.color = color
        DB.save(session, obj=project)
        return project

    @classmethod
    def project_delete(cls, session: orm.Session, project: Project):
        DB.delete(session=session, obj=project)
