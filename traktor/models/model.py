import enum
import uuid
from dataclasses import dataclass

import slugify
import sqlalchemy as sa
from sqlalchemy.engine import RowProxy
from sqlalchemy.ext.declarative import declarative_base

from traktor.timestamp import utcnow
from traktor.models.enums import Sort, RGB

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Align(str, enum.Enum):
    left = "left"
    center = "center"
    right = "right"


@dataclass
class Column:
    Align = Align

    title: str
    path: str
    align: str = "left"


class VanillaModel:
    HEADERS = []

    @classmethod
    def class_name(cls):
        return cls.__name__

    def to_dict(self) -> dict:
        return {}


class Model(Base):
    HEADERS = []

    __abstract__ = True

    Sort = Sort

    id = sa.Column(sa.String(36), default=generate_uuid, primary_key=True)

    # Timestamps
    created_on = sa.Column(sa.DateTime, default=utcnow)
    updated_on = sa.Column(sa.DateTime, default=utcnow, onupdate=utcnow)

    @classmethod
    def create(cls, **kwargs) -> "Model":
        model = cls(**kwargs)
        for column in cls.__table__.columns:
            if column.name not in kwargs and column.default is not None:
                if column.default.is_callable:
                    try:
                        setattr(model, column.name, column.default.arg(None))
                    except Exception:
                        pass
                else:
                    setattr(model, column.name, column.default.arg)
        return model

    @classmethod
    def class_name(cls):
        return cls.__name__

    def column_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def to_dict(self) -> dict:
        return self.column_dict()

    @classmethod
    def from_row(cls, row: RowProxy) -> "Model":
        return cls(
            **{
                column.name: getattr(row, column.name)
                for column in cls.__table__.columns
            }
        )


def _slugify_name(context):
    return slugify.slugify(context.get_current_parameters()["name"])


class Sluggable(Model):
    HEADERS = Model.HEADERS + [
        Column(title="ID", path="slug"),
        Column(title="Name", path="name"),
    ]

    __abstract__ = True

    name = sa.Column(sa.String(255), nullable=False)
    slug = sa.Column(
        sa.String(255), unique=True, nullable=False, default=_slugify_name
    )

    def rename(self, name: str):
        self.name = name
        self.slug = slugify.slugify(name)


class Colored(Sluggable):
    HEADERS = Sluggable.HEADERS + [
        Column(title="Color", path="rich_color", align=Column.Align.center)
    ]

    __abstract__ = True

    color = sa.Column(sa.String(7), nullable=False, default="#808080")

    @property
    def rich_color(self):
        c = RGB(self.color)
        return f"[{c.rich}]{self.color}[/{c.rich}]"
