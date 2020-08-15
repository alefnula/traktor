import enum
import uuid
from dataclasses import dataclass

import sqlalchemy as sa
from sqlalchemy.engine import RowProxy
from sqlalchemy.ext.declarative import declarative_base

from traktor.timestamp import utcnow
from traktor.models.enums import Sort, RGB
from traktor.timestamp import dt_to_str, str_to_dt

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

    @classmethod
    def from_dict(cls, d: dict) -> "VanillaModel":
        return cls()


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

    def to_db_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_on": dt_to_str(self.created_on),
            "updated_on": dt_to_str(self.updated_on),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Model":
        return cls(
            id=d["id"],
            created_on=str_to_dt(d["created_on"]),
            updated_on=str_to_dt(d["updated_on"]),
        )

    @classmethod
    def from_row(cls, row: RowProxy) -> "Model":
        return cls(
            id=row.id, created_on=row.created_on, updated_on=row.updated_on,
        )


class Colored(Model):
    HEADERS = Model.HEADERS + []

    __abstract__ = True

    color_hex = sa.Column(sa.String(7), nullable=False, default="#808080")

    @property
    def color(self) -> RGB:
        return RGB.parse(self.color_hex)

    @color.setter
    def color(self, value: RGB):
        self.color_hex = value.hex

    @property
    def rich_color(self):
        return f"[{self.color.rich}]{self.color.hex}[/{self.color.rich}]"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["color_hex"] = self.color_hex
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Colored":
        model = super().from_dict(d)
        model.color_hex = d["color_hex"]
        return model

    @classmethod
    def from_row(cls, row: RowProxy) -> "Colored":
        model = super().from_row(row)
        model.color_hex = row.color_hex
        return model
