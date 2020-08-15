from typing import List
from datetime import datetime, timedelta


from sqlalchemy import orm

from traktor import errors
from traktor.timestamp import utcnow, make_aware
from traktor.models import Entry, Report
from traktor.db.sync_db import SyncDB as DB
from traktor.engine.sync_engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    # Timer

    @classmethod
    def start(cls, session: orm.Session, project: str, task: str) -> Entry:
        # First see if there are running timers
        timer = DB.first(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        if timer is not None:
            raise errors.TimerAlreadyRunning(
                project=timer.project.name, task=timer.task.name
            )

        if task is None:
            task = cls.task_get_default(session=session, project=project)
            if task is None:
                raise errors.NoDefaultTask(project=project)
        else:
            task = cls.task_get(session=session, project=project, name=task)

        entry = Entry(project=task.project, task=task)
        DB.save(session=session, obj=entry)
        return entry

    @staticmethod
    def stop(session: orm.Session) -> List[Entry]:
        timers = DB.filter(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        for timer in timers:
            timer.stop()
            DB.save(session=session, obj=timer)

        return timers

    @staticmethod
    def status(session: orm.Session) -> List[Entry]:
        return DB.filter(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )

    @staticmethod
    def _make_report(entries: List[Entry]):
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
    def today(cls, session: orm.Session):
        dt = utcnow()
        today = make_aware(datetime(dt.year, dt.month, dt.day))
        return cls._make_report(
            DB.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > today],
            )
        )

    @classmethod
    def report(cls, session: orm.Session, days: int) -> List[Report]:
        if days == 0:
            entries = DB.all(session=session, model=Entry)
        else:
            dt = utcnow() - timedelta(days=days)
            since = make_aware(datetime(dt.year, dt.month, dt.day))
            entries = DB.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > since],
            )
        return cls._make_report(entries)
