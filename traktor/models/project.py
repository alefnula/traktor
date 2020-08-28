from django.db import models

from tea_console.table import Column
from tea_django.models import UUIDBaseModel
from tea_django.models.mixins import (
    ColoredMixin,
    NonUniqueSlugMixin,
    TimestampedMixin,
)
from traktor.models.user import User


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")


class Project(
    UUIDBaseModel, ColoredMixin, NonUniqueSlugMixin, TimestampedMixin
):
    HEADERS = [
        Column(title="ID", path="slug"),
        Column(title="Name", path="rich_name"),
    ]
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        default=User.get_superuser_id,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    @property
    def rich_name(self) -> str:
        return self.rich(self.name)

    def __str__(self):
        return f"{self.name}"

    __repr__ = __str__

    objects = ProjectManager()

    class Meta:
        app_label = "traktor"
        unique_together = ("user", "slug")
