import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.engine import RowProxy

from traktor.models.model import Colored, Column


class Task(Colored):
    HEADERS = Colored.HEADERS + [
        Column(title="Project", path="project.name"),
        Column(title="Name", path="name"),
        Column(title="Color", path="rich_color", align=Column.Align.center),
        Column(title="Default", path="default", align=Column.Align.center),
    ]

    __tablename__ = "task"
    _table_args__ = (
        sa.UniqueConstraint(
            "project_id",
            "name",
            name="task_project_id_task_name_unique_constraint",
        ),
    )

    project_id = sa.Column(
        sa.String(36), sa.ForeignKey("project.id", ondelete="CASCADE")
    )
    name = sa.Column(sa.String(127), nullable=False)
    default = sa.Column(sa.Boolean, default=False)

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
            f"color={self.color_hex})"
        )

    __repr__ = __str__

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "project_id": self.project_id,
                "name": self.name,
                "default": self.default,
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        model = super().from_dict(d)
        model.project_id = d["project_id"]
        model.name = d["name"]
        model.default = d["default"]
        return model

    @classmethod
    def from_row(cls, row: RowProxy) -> "Task":
        model = super().from_row(row)
        model.project_id = row.project_id
        model.name = row.name
        model.default = row.default
        return model
