from django.db import models

from tea import timestamp as ts
from tea_console.table import Column
from tea_django.models import UUIDBaseModel
from tea_django.models.mixins import TimestampedMixin, TimerMixin

from traktor.models.project import Project
from traktor.models.task import Task


class Entry(UUIDBaseModel, TimestampedMixin, TimerMixin):
    HEADERS = [
        Column(title="Project", path="project.name"),
        Column(title="Task", path="task.name"),
        Column(
            title="Start Time",
            path=lambda o: ts.to_localtime_str(o.start_time),
        ),
        Column(
            title="End Time", path=lambda o: ts.to_localtime_str(o.end_time),
        ),
        Column(title="Duration", path="running_time"),
    ]

    project = models.ForeignKey(
        Project, null=False, blank=False, on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        Task, null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.CharField(
        max_length=1023, null=False, blank=True, default=""
    )
    notes = models.TextField(null=False, blank=True, default="")

    def __str__(self):
        return (
            f"Entry(project={self.project.slug}, "
            f"task={self.task.slug if self.task is not None else None}, "
            f"running_time={self.running_time})"
        )

    __repr__ = __str__

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "project": self.project.slug,
                "task": self.task.slug,
                "running_time": self.running_time,
            }
        )
        return d

    class Meta:
        app_label = "traktor"
