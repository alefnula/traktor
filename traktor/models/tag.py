from sqlalchemy import orm

from traktor.models.model import Colored
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
