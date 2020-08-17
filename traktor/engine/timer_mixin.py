from typing import List, Optional
from datetime import datetime, timedelta

from django.utils import timezone


from traktor import errors
from traktor.models import Entry, Report
from traktor.engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    # Timer

    @classmethod
    def timer_start(
        cls, project_id: str, task_id: Optional[str] = None
    ) -> Entry:
        # First see if there are running timers
        entry = Entry.objects.filter(end_time=None).first()
        if entry is not None:
            raise errors.TimerAlreadyRunning(
                project_id=entry.project.slug, task_id=entry.task.slug
            )

        if task_id is None:
            task = cls.task_get_default(project_id=project_id)
            if task is None:
                raise errors.NoDefaultTask(project_id=project_id)
        else:
            task = cls.task_get(project_id=project_id, task_id=task_id)

        return Entry.objects.create(project=task.project, task=task)

    @staticmethod
    def timer_stop() -> Entry:
        entry = Entry.objects.filter(end_time=None).first()
        if entry is None:
            raise errors.TimerIsNotRunning()

        entry.stop()
        entry.save()
        return entry

    @staticmethod
    def timer_status() -> Optional[Entry]:
        return Entry.objects.filter(end_time=None).first()

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
    def timer_today(cls):
        now = timezone.now()
        today = timezone.make_aware(datetime(now.year, now.month, now.day))
        return cls._make_report(Entry.objects.filter(start_time__gt=today))

    @classmethod
    def timer_report(cls, days: int) -> List[Report]:
        if days == 0:
            entries = Entry.objects.all()
        else:
            dt = timezone.now() - timedelta(days=days)
            since = timezone.make_aware(datetime(dt.year, dt.month, dt.day))
            entries = Entry.objects.filter(start_time__gt=since)
        return cls._make_report(entries)
