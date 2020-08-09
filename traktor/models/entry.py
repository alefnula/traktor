from typing import Optional
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from traktor.config import config
from traktor import timestamp as ts
from traktor.models.model import Model, Column
from traktor.models.entry_tag import entry_tag_table


class Entry(Model):
    HEADERS = Model.HEADERS + [
        Column(title="Project", path="project.name"),
        Column(title="Task", path="task.name"),
        Column(
            title="Start Time",
            path="local_start_time",
            align=Column.Align.center,
        ),
        Column(
            title="End Time", path="local_end_time", align=Column.Align.center
        ),
        Column(
            title="Duration", path="running_time", align=Column.Align.center
        ),
    ]

    __tablename__ = "entry"

    project_id = sa.Column(
        sa.String(36), sa.ForeignKey("project.id", ondelete="CASCADE")
    )
    task_id = sa.Column(
        sa.String(36), sa.ForeignKey("task.id", ondelete="CASCADE")
    )

    description = sa.Column(sa.String(2047), nullable=False, default="")
    notes = sa.Column(sa.String, nullable=False, default="")

    # Timestamps
    start_time = sa.Column(sa.DateTime, nullable=False, default=ts.utcnow)
    end_time = sa.Column(sa.DateTime, nullable=True, default=None)
    duration = sa.Column(sa.BigInteger, nullable=False, default=0)

    @property
    def local_start_time(self) -> str:
        return ts.local_time(
            ts.make_aware(self.start_time), config.timezone
        ).strftime("%Y.%m.%d %H:%M:%S")

    @property
    def local_end_time(self) -> Optional[datetime]:
        if self.end_time is None:
            return None
        return ts.local_time(
            ts.make_aware(self.end_time), config.timezone
        ).strftime("%Y.%m.%d %H:%M:%S")

    @property
    def running_time(self) -> str:
        if self.end_time is not None:
            end_time = ts.make_aware(self.end_time)
        else:
            end_time = ts.utcnow()

        return ts.humanize(
            int((end_time - ts.make_aware(self.start_time)).total_seconds())
        )

    def stop(self):
        self.end_time = ts.utcnow()
        self.duration = int(
            (
                ts.make_aware(self.end_time) - ts.make_aware(self.start_time)
            ).total_seconds()
        )

    # Relationships
    tags = orm.relationship(
        "Tag",
        secondary=entry_tag_table,
        back_populates="entries",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __str__(self):
        return (
            f"Task(project={self.project.name}, name={self.name}, "
            f"color={self.color})"
        )

    __repr__ = __str__

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update(
            {
                "project_id": self.project_id,
                "task_id": self.task_id,
                "description": self.description,
                "notes": self.notes,
                "start_time": ts.dt_to_str(self.start_time),
                "end_time": ts.dt_to_str(self.end_time),
                "duration": self.duration,
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Entry":
        model = super().from_dict(d)
        model.project_id = d["project_id"]
        model.task_id = d["task_id"]
        model.description = d["description"]
        model.notes = d["notes"]
        model.start_time = ts.str_to_dt(d["start_time"])
        model.end_time = ts.str_to_dt(d["end_time"])
        model.duration = d["duration"]
        return model
