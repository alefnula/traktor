from uuid import UUID
from typing import List

from traktor.models import Tag
from traktor.db.async_db import async_db as db


class TagMixin:
    @staticmethod
    async def tag_list() -> List[Tag]:
        return await db.all(model=Tag)

    @staticmethod
    async def tag_get(tag_id: str) -> Tag:
        try:
            UUID(tag_id)
            return await db.get_by_id(model=Tag, obj_id=tag_id)
        except ValueError:
            return await db.get(model=Tag, filters=[Tag.name == tag_id])

    @classmethod
    async def tag_delete(cls, tag_id: str) -> bool:
        tag = await cls.tag_get(tag_id=tag_id)
        return await db.delete(obj=tag)
