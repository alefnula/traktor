import sqlalchemy as sa
from sqlalchemy import orm

from traktor.models.model import Colored, Column, slugify_name


class Task(Colored):
    HEADERS = (
        [Column(title="Project ID", path="project.slug")]
        + Colored.HEADERS
        + [Column(title="Default", path="default", align=Column.Align.center)]
    )

    __tablename__ = "task"
    __table_args__ = (
        sa.UniqueConstraint(
            "project_id",
            "slug",
            name="task_project_id_task_slug_unique_constraint",
        ),
    )

    slug = sa.Column(sa.String(255), nullable=False, default=slugify_name)
    project_id = sa.Column(
        sa.String(36), sa.ForeignKey("project.id", ondelete="CASCADE")
    )
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
            f"color={self.color})"
        )

    __repr__ = __str__
