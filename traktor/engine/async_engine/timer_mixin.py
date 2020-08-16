from typing import List, Optional
from datetime import datetime, timedelta

from traktor import errors
from traktor import timestamp as ts
from traktor.models import Entry, Report
from traktor.db.async_db import async_db as db
from traktor.engine.async_engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    @classmethod
    async def _populate_entry(cls, entry: Entry) -> Entry:
        entry.project = await cls.project_get_by_uuid(
            project_id=entry.project_id
        )
        entry.task = await cls.task_get_by_uuid(task_id=entry.task_id)
        return entry

    @classmethod
    async def timer_start(
        cls, project_id: str, task_id: Optional[str] = None
    ) -> Entry:
        # First see if there are running timers
        timer = await db.first(model=Entry, filters=[Entry.end_time.is_(None)])
        if timer is not None:
            raise errors.TimerAlreadyRunning(
                project_id=timer.project.slug, task_id=timer.task.slug
            )
        if task_id is None:
            task = await cls.task_get_default(project_id=project_id)
            if task is None:
                raise errors.NoDefaultTask(project_id=project_id)
        else:
            task = cls.task_get(project_id=project_id, task_id=task_id)

        entry = Entry.create(project_id=task.project_id, task_id=task.id)
        entry = await db.save(entry)
        return await cls._populate_entry(entry)

    @classmethod
    async def timer_stop(cls) -> Entry:
        entry = await db.first(model=Entry, filters=[Entry.end_time.is_(None)])
        if entry is None:
            raise errors.TimerIsNotRunning()

        entry.stop()
        entry = await db.update(entry)
        return await cls._populate_entry(entry=entry)

    @classmethod
    async def timer_status(cls) -> Optional[Entry]:
        entry = await db.first(model=Entry, filters=[Entry.end_time.is_(None)])
        if entry is None:
            return None
        return await cls._populate_entry(entry=entry)

    @classmethod
    async def _make_report(cls, entries: List[Entry]):
        reports = {}
        for entry in entries:
            entry = await cls._populate_entry(entry)

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
    async def timer_today(cls):
        dt = ts.utcnow()
        today = ts.make_aware(datetime(dt.year, dt.month, dt.day))
        return await cls._make_report(
            await db.filter(model=Entry, filters=[Entry.start_time > today])
        )

    @classmethod
    async def timer_report(cls, days: int) -> List[Report]:
        if days == 0:
            entries = await db.all(model=Entry)
        else:
            dt = ts.utcnow() - timedelta(days=days)
            since = ts.make_aware(datetime(dt.year, dt.month, dt.day))
            entries = await db.filter(
                model=Entry, filters=[Entry.start_time > since]
            )
        return await cls._make_report(entries)
