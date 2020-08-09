import sqlalchemy as sa
from sqlalchemy import orm

from tracker.models.model import Colored
from tracker.models.entry_tag import entry_tag_table


class Tag(Colored):
    HEADERS = Colored.HEADERS + [("Name", "name"), ("Color", "rich_color")]

    __tablename__ = "tag"

    name = sa.Column(sa.String(127), unique=True, nullable=False)

    # Relationships
    entries = orm.relationship(
        "Entry",
        secondary=entry_tag_table,
        back_populates="tags",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self):
        return f"Tag(name={self.name}, color={self.color_hex})"

    __repr__ = __str__

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["name"] = self.name
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Tag":
        model = super().from_dict(d)
        model.name = d["name"]
        return model
