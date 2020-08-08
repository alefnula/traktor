import sqlalchemy as sa

from tracker.models.model import Base

entry_tag_table = sa.Table(
    "entry_tag",
    Base.metadata,
    sa.Column("entry_id", sa.String(36), sa.ForeignKey("entry.id")),
    sa.Column("tag_id", sa.String(36), sa.ForeignKey("tag.id")),
)
