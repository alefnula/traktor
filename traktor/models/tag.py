from typing import Optional

import slugify
from sqlalchemy import orm
from pydantic import BaseModel, validator

from traktor.models.model import RGB, Colored
from traktor.models.entry_tag import entry_tag_table


class Tag(Colored):
    __tablename__ = "tag"

    # Relationships
    entries = orm.relationship(
        "Entry",
        secondary=entry_tag_table,
        back_populates="tags",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self):
        return f"Tag(name={self.name}, color={self.color})"

    __repr__ = __str__


class TagCreateRequest(BaseModel):
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


class TagUpdateRequest(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

    @validator("color")
    def validate_color(cls, value):
        if value is None:
            return None
        c = RGB(value)
        return c.hex
