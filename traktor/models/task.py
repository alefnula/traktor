from django.db import models

from console_tea.table import Column
from django_tea.models import UUIDBaseModel
from django_tea.models.mixins import (
    ColoredMixin,
    NonUniqueSlugMixin,
    TimestampedMixin,
)

from traktor.models.project import Project


class Task(UUIDBaseModel, ColoredMixin, NonUniqueSlugMixin, TimestampedMixin):
    HEADERS = [
        Column(title="Project ID", path="project.slug"),
        Column(title="Task ID", path="slug"),
        Column(title="Name", path="rich_name"),
        Column(title="Default", path="default"),
    ]

    project = models.ForeignKey(
        Project, blank=False, null=False, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    default = models.BooleanField(default=False, blank=False, null=False)

    @property
    def rich_name(self) -> str:
        return self.rich(self.name)

    def __str__(self):
        return f"{self.project.name} / {self.name})"

    __repr__ = __str__

    class Meta:
        app_label = "traktor"
        unique_together = [["project", "slug"]]
