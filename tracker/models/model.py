import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from tracker.timestamp import utcnow
from tracker.models.enums import Sort

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Model(Base):
    __abstract__ = True

    Sort = Sort

    id = Column(String(36), default=generate_uuid, primary_key=True)

    # Timestamps
    created_on = Column(DateTime, default=utcnow)
    updated_on = Column(DateTime, default=utcnow, onupdate=utcnow)
