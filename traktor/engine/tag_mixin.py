from typing import List, Optional


from sqlalchemy import orm

from traktor import errors
from traktor.models import DB, RGB, Task, Tag


class TagMixin:
    @staticmethod
    def tag_list(session: orm.Session) -> List[Tag]:
        """List all tags.

        Args:
            session (orm.Session): SQLAlchemy session.
        """
        return DB.all(session=session, model=Task)

    @staticmethod
    def tag_get(session: orm.Session, name: str) -> Tag:
        return DB.get(session=session, model=Tag, filters=[Tag.name == name])

    @classmethod
    def tag_get_or_create(
        cls, session: orm.Session, name: str, color: Optional[RGB] = None,
    ) -> Tag:
        try:
            obj = cls.tag_get(session=session, name=name)
            if color is not None:
                if obj.color != color:
                    obj.color = color
                    DB.save(session=session, obj=obj)

        except errors.ObjectNotFound:
            obj = Tag(name=name, color_hex=(color or RGB()).hex,)
            DB.save(session=session, obj=obj)

        return obj

    @classmethod
    def tag_update(
        cls,
        session: orm.Session,
        tag: str,
        name: Optional[str],
        color: Optional[RGB],
    ) -> Tag:
        tag = cls.tag_get(session=session, name=tag)
        # Change name
        if name is not None:
            tag.name = name
        # Change color
        if color is not None:
            tag.color = color
        DB.save(session, obj=tag)
        return tag

    @staticmethod
    def tag_delete(session: orm.Session, tag: Tag):
        DB.delete(session=session, obj=tag)
