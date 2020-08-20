from django.db import models

from django_tea.table import Column
from django_tea.models import UUIDBaseModel
from django_tea.models.mixins import (
    ColoredMixin,
    UniqueSlugMixin,
    TimestampedMixin,
)


class Project(UUIDBaseModel, ColoredMixin, UniqueSlugMixin, TimestampedMixin):
    HEADERS = [
        Column(title="ID", path="slug"),
        Column(title="Name", path="rich_name"),
    ]

    name = models.CharField(max_length=255)

    @property
    def rich_name(self) -> str:
        return self.rich(self.name)

    def __str__(self):
        return f"{self.name}"

    __repr__ = __str__

    class Meta:
        app_label = "traktor"
