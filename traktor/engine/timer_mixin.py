from typing import List, Optional
from datetime import datetime, timedelta

from tea import timestamp as ts

from traktor import errors
from traktor.models import User, Entry, Report
from traktor.engine.task_mixin import TaskMixin


class TimerMixin(TaskMixin):
    # Timer

    @classmethod
    def timer_start(
        cls, user: User, project_id: str, task_id: Optional[str] = None
    ) -> Entry:
        # First see if there are running timers
        entry = Entry.objects.filter(
            task__project__user=user, end_time=None
        ).first()
        if entry is not None:
            raise errors.TimerAlreadyRunning(
                project_id=entry.task.project.slug, task_id=entry.task.slug
            )

        if task_id is None:
            task = cls.task_get_default(user=user, project_id=project_id)
            if task is None:
                raise errors.NoDefaultTask(
                    user=user.username, project_id=project_id
                )
        else:
            task = cls.task_get(
                user=user, project_id=project_id, task_id=task_id
            )

        return Entry.objects.create(task=task)

    @staticmethod
    def timer_stop(user: User) -> Entry:
        entry = Entry.objects.filter(
            task__project__user=user, end_time=None
        ).first()
        if entry is None:
            raise errors.TimerIsNotRunning()

        entry.stop()
        entry.save()
        return entry

    @staticmethod
    def timer_status(user: User) -> Optional[Entry]:
        entry = Entry.objects.filter(
            task__project__user=user, end_time=None
        ).first()
        if entry is None:
            raise errors.TimerIsNotRunning()
        return entry

    @staticmethod
    def _make_report(entries: List[Entry]) -> List[Report]:
        reports = {}
        for entry in entries:
            report = Report(
                user=entry.task.project.user.username,
                project=entry.task.project.name,
                task=entry.task.name,
                duration=(
                    entry.duration
                    or int((ts.now() - entry.start_time).total_seconds())
                ),
            )
            if report.key in reports:
                reports[report.key].duration += report.duration
            else:
                reports[report.key] = report
        return list(reports.values())

    @classmethod
    def timer_today(cls, user: User):
        now = ts.now()
        today = ts.make_aware(datetime(now.year, now.month, now.day))
        return cls._make_report(
            Entry.objects.filter(
                task__project__user=user, start_time__gt=today
            )
        )

    @classmethod
    def timer_report(cls, user: User, days: int = 0) -> List[Report]:
        if days == 0:
            entries = Entry.objects.filter(task__project__user=user)
        else:
            dt = ts.now() - timedelta(days=days)
            since = ts.make_aware(datetime(dt.year, dt.month, dt.day))
            entries = Entry.objects.filter(
                task__project__user=user, start_time__gt=since
            )
        return cls._make_report(entries)
