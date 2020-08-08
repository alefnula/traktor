from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm

from tracker.models.db import db
from tracker.models.enums import RGB
from tracker.models.model import Colored
from tracker.models.project import Project


class Task(Colored):
    __tablename__ = "task"
    _table_args__ = (
        sa.UniqueConstraint(
            "project_id",
            "name",
            name="task_project_id_task_name_unique_constraint",
        ),
    )

    project_id = sa.Column(sa.String(36), sa.ForeignKey("project.id"))
    name = sa.Column(sa.String(127), nullable=False)

    # Relationships
    entries = orm.relationship(
        "Entry", backref="tasks", order_by="asc(Entry.start_time)"
    )

    @classmethod
    def get_or_create(
        cls,
        session: orm.Session,
        project: Project,
        name: str,
        color: Optional[RGB] = None,
    ) -> "Task":
        obj: "Task" = db.first(
            session=session,
            model=cls,
            filters=[cls.project_id == project.id, cls.name == name],
        )
        if obj is not None:
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    db.save(obj)
        else:
            obj = cls(
                project_id=project.id,
                name=name,
                color_hex=(color or RGB()).hex,
            )
            db.save(session=session, obj=obj)

        return obj

    def __str__(self):
        return (
            f"Task(project={self.project.name}, name={self.name}, "
            f"color={self.color_hex})"
        )

    __repr__ = __str__

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["project_id"] = self.project_id
        d["name"] = self.name
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        model = super().from_dict(d)
        model.project_id = d["project_id"]
        model.name = d["name"]
        return model
