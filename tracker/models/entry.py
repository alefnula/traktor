import sqlalchemy as sa
from sqlalchemy import orm

from tracker.timestamp import utcnow
from tracker.models.model import Model
from tracker.models.entry_tag import entry_tag_table


class Entry(Model):
    __tablename__ = "entry"

    project_id = sa.Column(sa.String(36), sa.ForeignKey("project.id"))
    task_id = sa.Column(sa.String(36), sa.ForeignKey("task.id"))

    description = sa.Column(sa.String(2047), nullable=False, default="")
    notes = sa.Column(sa.String, nullable=False, default="")

    # Timestamps
    start_time = sa.Column(sa.DateTime, nullable=False, default=utcnow)
    end_time = sa.Column(sa.DateTime, nullable=True, default=None)
    duration = sa.Column(sa.BigInteger, nullable=False, default=0)

    # Relationships
    tags = orm.relationship(
        "Tag", secondary=entry_tag_table, back_populates="entries"
    )

    def __str__(self):
        return (
            f"Task(project={self.project.name}, name={self.name}, "
            f"color={self.color})"
        )

    __repr__ = __str__
