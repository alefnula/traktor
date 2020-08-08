from typing import List, Optional

from sqlalchemy import orm


from tracker.models import db, RGB, Project


class Engine:
    @staticmethod
    def project_list(session: orm.Session) -> List[Project]:
        return db.all(session=session, model=Project)

    @staticmethod
    def project_get(session: orm.Session, name: str) -> Optional[Project]:
        return db.first(
            session=session, model=Project, filters=[Project.name == name]
        )

    @classmethod
    def project_get_or_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None
    ) -> Project:
        obj = cls.project_get(session=session, name=name)
        if obj is not None:
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    db.save(obj)
        else:
            obj = Project(name=name, color_hex=(color or RGB()).hex)
            db.save(session=session, obj=obj)

        return obj

    @staticmethod
    def project_delete(session: orm.Session, project: Project):
        db.delete(session=session, obj=project)


engine = Engine()
