from typing import List, Optional
from datetime import datetime, timedelta


from sqlalchemy import orm

from traktor import errors
from traktor import timestamp as ts
from traktor.models import Entry, Report
from traktor.db.sync_db import sync_db as db
from traktor.engine.sync_engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    # Timer

    @classmethod
    def timer_start(
        cls,
        session: orm.Session,
        project_id: str,
        task_id: Optional[str] = None,
    ) -> Entry:
        # First see if there are running timers
        timer = db.first(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        if timer is not None:
            raise errors.TimerAlreadyRunning(
                project_id=timer.project.slug, task_id=timer.task.slug
            )

        if task_id is None:
            task = cls.task_get_default(session=session, project_id=project_id)
            if task is None:
                raise errors.NoDefaultTask(project_id=project_id)
        else:
            task = cls.task_get(
                session=session, project_id=project_id, task_id=task_id
            )

        entry = Entry(project=task.project, task=task)
        return db.save(session=session, obj=entry)

    @staticmethod
    def timer_stop(session: orm.Session) -> Entry:
        timer = db.first(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        if timer is None:
            raise errors.TimerIsNotRunning()

        timer.stop()
        db.save(session=session, obj=timer)
        return timer

    @staticmethod
    def timer_status(session: orm.Session) -> Entry:
        return db.first(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )

    @staticmethod
    def _make_report(entries: List[Entry]) -> List[Report]:
        reports = {}
        for entry in entries:
            report = Report(
                project=entry.project.name,
                task=entry.task.name,
                duration=entry.duration,
            )
            if report.key in reports:
                reports[report.key].duration += report.duration
            else:
                reports[report.key] = report
        return list(reports.values())

    @classmethod
    def timer_today(cls, session: orm.Session):
        dt = ts.utcnow()
        today = ts.make_aware(datetime(dt.year, dt.month, dt.day))
        return cls._make_report(
            db.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > today],
            )
        )

    @classmethod
    def timer_report(cls, session: orm.Session, days: int) -> List[Report]:
        if days == 0:
            entries = db.all(session=session, model=Entry)
        else:
            dt = ts.utcnow() - timedelta(days=days)
            since = ts.make_aware(datetime(dt.year, dt.month, dt.day))
            entries = db.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > since],
            )
        return cls._make_report(entries)
