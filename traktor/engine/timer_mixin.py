from typing import List
from datetime import datetime, timedelta


from sqlalchemy import orm

from traktor import errors
from traktor.timestamp import utcnow, make_aware
from traktor.models import DB, Entry, Report
from traktor.engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    # Timer

    @classmethod
    def start(cls, session: orm.Session, project: str, task: str) -> Entry:
        # First see if there are running timers
        timers = DB.filter(
            session=session, model=Entry, filters=[Entry.end_time.is_(None)]
        )
        if len(timers) > 0:
            raise errors.TimerAlreadyRunning(timers)

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
    def status(session: orm.Session):
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
            DB.filter(
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
            DB.filter(
                session=session,
                model=Entry,
                filters=[Entry.start_time > since],
            )
        )
