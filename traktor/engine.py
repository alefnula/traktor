from typing import List, Optional
from datetime import datetime, timedelta


from sqlalchemy import orm

from traktor import errors
from traktor.timestamp import utcnow, make_aware
from traktor.models import db, RGB, Project, Task, Tag, Entry, Report


class Engine:
    # Timer

    @classmethod
    def start(cls, session: orm.Session, project: str, task: str) -> Entry:
        # First see if there are running timers
        timers = db.filter(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        if len(timers) > 0:
            raise errors.TimerAlreadyRunning(timers)

        project = cls.project_get(session=session, name=project)
        task = cls.task_get(session=session, project=project.name, name=task)
        entry = Entry(project=project, task=task)
        db.save(session=session, obj=entry)
        return entry

    @staticmethod
    def stop(session: orm.Session) -> List[Entry]:
        timers = db.filter(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        for timer in timers:
            timer.stop()
            db.save(session=session, obj=timer)

        return timers

    @staticmethod
    def status(session: orm.Session):
        return db.filter(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )

    @staticmethod
    def _make_report(entries: List[Entry]):
        reports = {}
        for entry in entries:
            report = Report(
                project=entry.project.name,
                task=entry.task.name,
                time=entry.duration,
            )
            if report.key in reports:
                reports[report.key].time += report.time
            else:
                reports[report.key] = report
        return list(reports.values())

    @classmethod
    def today(cls, session: orm.Session):
        dt = utcnow()
        today = make_aware(datetime(dt.year, dt.month, dt.day))
        return cls._make_report(
            db.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > today],
            )
        )

    @classmethod
    def report(cls, session: orm.Session, days: int) -> List[Report]:
        dt = utcnow() - timedelta(days=days)
        since = make_aware(datetime(dt.year, dt.month, dt.day))
        return cls._make_report(
            db.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > since],
            )
        )

    # Project

    @staticmethod
    def project_list(session: orm.Session) -> List[Project]:
        return db.all(session=session, model=Project)

    @staticmethod
    def project_get(session: orm.Session, name: str) -> Project:
        return db.get(
            session=session, model=Project, filters=[Project.name == name]
        )

    @classmethod
    def project_get_or_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None
    ) -> Project:
        try:
            obj = cls.project_get(session=session, name=name)
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    db.save(session=session, obj=obj)
        except errors.ObjectNotFound:
            obj = Project(name=name, color_hex=(color or RGB()).hex)
            db.save(session=session, obj=obj)

        return obj

    @classmethod
    def project_rename(
        cls, session: orm.Session, name: str, new_name: str
    ) -> Project:
        project = cls.project_get(session=session, name=name)
        project.name = new_name
        db.save(session=session, obj=project)
        return project

    @classmethod
    def project_delete(cls, session: orm.Session, project: Project):
        db.delete(session=session, obj=project)

    # Task

    @classmethod
    def task_list(cls, session: orm.Session, project: str) -> List[Task]:
        """List all tasks in a project.

        Args:
            session (orm.Session): SQLAlchemy session.
            project (str): Project name.
        """
        project = cls.project_get(session=session, name=project)

        return db.filter(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id],
        )

    @classmethod
    def task_get(cls, session: orm.Session, project: str, name: str) -> Task:
        project = cls.project_get(session=session, name=project)
        return db.get(
            session=session,
            model=Task,
            filters=[Task.project_id == project.id, Task.name == name],
        )

    @classmethod
    def task_get_or_create(
        cls,
        session: orm.Session,
        project: str,
        name: str,
        color: Optional[RGB] = None,
    ) -> Task:
        project = cls.project_get(session=session, name=project)
        try:
            obj = cls.task_get(
                session=session, project=project.name, name=name
            )
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    db.save(session=session, obj=obj)

        except errors.ObjectNotFound:
            obj = Task(
                project_id=project.id,
                name=name,
                color_hex=(color or RGB()).hex,
            )
            db.save(session=session, obj=obj)

        return obj

    @classmethod
    def task_rename(
        cls, session: orm.Session, project: str, name: str, new_name: str
    ) -> Task:
        task = cls.task_get(session=session, project=project, name=name)
        task.name = new_name
        db.save(session=session, obj=task)
        return task

    @staticmethod
    def task_delete(session: orm.Session, task: Task):
        db.delete(session=session, obj=task)

    # Tag

    @staticmethod
    def tag_list(session: orm.Session) -> List[Tag]:
        """List all tags.

        Args:
            session (orm.Session): SQLAlchemy session.
        """
        return db.all(session=session, model=Task)

    @staticmethod
    def tag_get(session: orm.Session, name: str) -> Tag:
        return db.get(session=session, model=Tag, filters=[Tag.name == name])

    @classmethod
    def tag_get_or_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None,
    ) -> Tag:
        try:
            obj = cls.tag_get(session=session, name=name)
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    db.save(session=session, obj=obj)

        except errors.ObjectNotFound:
            obj = Tag(name=name, color_hex=(color or RGB()).hex,)
            db.save(session=session, obj=obj)

        return obj

    @classmethod
    def tag_rename(
        cls, session: orm.Session, name: str, new_name: str
    ) -> Project:
        tag = cls.tag_get(session=session, name=name)
        tag.name = new_name
        db.save(session=session, obj=tag)
        return tag

    @staticmethod
    def tag_delete(session: orm.Session, tag: Tag):
        db.delete(session=session, obj=tag)


engine = Engine()
