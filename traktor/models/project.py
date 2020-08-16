from typing import Optional

import slugify
from sqlalchemy import orm
from pydantic import BaseModel, validator

from traktor.models.model import RGB, Colored


class Project(Colored):
    __tablename__ = "project"

    # Relationships
    tasks = orm.relationship(
        "Task",
        backref="project",
        order_by="asc(Task.name)",
        cascade="all, delete",
        passive_deletes=True,
    )
    entries = orm.relationship(
        "Entry",
        backref="project",
        order_by="asc(Entry.start_time)",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self):
        return f"Project(name={self.name}, color={self.color})"

    __repr__ = __str__


class ProjectCreateRequest(BaseModel):
    name: str
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return RGB().hex
        c = RGB(value)
        return c.hex

    @property
    def slug(self):
        return slugify.slugify(self.name)


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return None
        c = RGB(value)
        return c.hex
