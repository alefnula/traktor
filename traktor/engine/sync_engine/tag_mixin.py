from typing import List, Optional

import slugify
from sqlalchemy import orm

from traktor import errors
from traktor.models import RGB, Tag
from traktor.db.sync_db import sync_db as db


class TagMixin:
    @staticmethod
    def tag_list(session: orm.Session) -> List[Tag]:
        """List all tags.

        Args:
            session (orm.Session): SQLAlchemy session.
        """
        return db.all(session=session, model=Tag)

    @staticmethod
    def tag_get(session: orm.Session, tag_id: str) -> Tag:
        return db.get(session=session, model=Tag, filters=[Tag.slug == tag_id])

    @classmethod
    def tag_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None,
    ) -> Tag:
        try:
            cls.tag_get(session=session, tag_id=slugify.slugify(name))
            raise errors.ObjectAlreadyExists(model=Tag, query={"name": name})
        except errors.ObjectNotFound:
            obj = Tag(name=name, color=(color or RGB()).hex,)
            db.save(session=session, obj=obj)

        return obj

    @classmethod
    def tag_update(
        cls,
        session: orm.Session,
        tag_id: str,
        name: Optional[str],
        color: Optional[RGB],
    ) -> Tag:
        tag = cls.tag_get(session=session, tag_id=tag_id)
        # Change name
        if name is not None:
            tag.rename(name)
        # Change color
        if color is not None:
            tag.color = color
        db.save(session, obj=tag)
        return tag

    @classmethod
    def tag_delete(cls, session: orm.Session, tag_id: str):
        tag = cls.tag_get(session=session, tag_id=tag_id)
        db.delete(session=session, obj=tag)
