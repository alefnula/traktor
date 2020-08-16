from typing import Optional

import slugify
import sqlalchemy as sa
from sqlalchemy import orm
from pydantic import BaseModel, validator

from traktor.models.model import RGB, Colored, Column, slugify_name


class Task(Colored):
    HEADERS = (
        [Column(title="Project ID", path="project.slug")]
        + Colored.HEADERS
        + [Column(title="Default", path="default", align=Column.Align.center)]
    )

    __tablename__ = "task"
    __table_args__ = (
        sa.UniqueConstraint(
            "project_id",
            "slug",
            name="task_project_id_task_slug_unique_constraint",
        ),
    )

    slug = sa.Column(sa.String(255), nullable=False, default=slugify_name)
    project_id = sa.Column(
        sa.String(36),
        sa.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False,
    )
    default = sa.Column(sa.Boolean, default=False, nullable=False)

    # Relationships
    entries = orm.relationship(
        "Entry",
        backref="task",
        order_by="asc(Entry.start_time)",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self):
        return (
            f"Task(project={self.project.name}, name={self.name}, "
            f"color={self.color})"
        )

    __repr__ = __str__


class TaskCreateRequest(BaseModel):
    name: str
    color: Optional[str] = None
    default: bool = False

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return RGB().hex
        c = RGB(value)
        return c.hex

    @property
    def slug(self):
        return slugify.slugify(self.name)


class TaskUpdateRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    default: Optional[bool] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return None
        c = RGB(value)
        return c.hex
