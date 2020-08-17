from django.db import models

from django_tea.table import Column
from django_tea import timestamp as ts
from django_tea.models import UUIDBaseModel
from django_tea.models.mixins import TimestampedMixin, TimerMixin

from traktor.models.project import Project
from traktor.models.task import Task


class Entry(UUIDBaseModel, TimestampedMixin, TimerMixin):
    HEADERS = [
        Column(title="Project", path="project.name"),
        Column(title="Task", path="task.name"),
        Column(
            title="Start Time",
            path=lambda o: ts.time_to_local_str(o.start_time),
        ),
        Column(
            title="End Time", path=lambda o: ts.time_to_local_str(o.end_time),
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
        max_length=1023, null=False, blank=False, default=""
    )
    notes = models.TextField(null=False, blank=False, default="")

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
