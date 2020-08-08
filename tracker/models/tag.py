import sqlalchemy as sa
from sqlalchemy import orm

from tracker.models.model import Colored
from tracker.models.entry_tag import entry_tag_table


class Tag(Colored):
    __tablename__ = "tag"

    name = sa.Column(sa.String(127), unique=True, nullable=False)

    # Relationships
    entries = orm.relationship(
        "Entry", secondary=entry_tag_table, back_populates="tags"
    )

    def __str__(self):
        return f"Tag(name={self.name}, color={self.color_hex})"

    __repr__ = __str__
