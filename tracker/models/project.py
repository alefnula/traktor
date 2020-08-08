import sqlalchemy as sa
from sqlalchemy import orm

from tracker.models.model import Colored


class Project(Colored):
    HEADERS = Colored.HEADERS + ["name", "color"]

    __tablename__ = "project"

    name = sa.Column(sa.String(127), unique=True, nullable=False)

    # Relationships
    tasks = orm.relationship(
        "Task", backref="project", order_by="asc(Task.name)"
    )
    entries = orm.relationship(
        "Entry", backref="project", order_by="asc(Entry.start_time)"
    )

    def __str__(self):
        return f"Project(name={self.name}, color={self.color_hex})"

    __repr__ = __str__

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["name"] = self.name
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Project":
        model = super().from_dict(d)
        model.name = d["name"]
        return model
