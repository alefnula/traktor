from typing import List

from traktor import errors
from traktor.models import RGB, Tag, TagCreateRequest, TagUpdateRequest
from traktor.db.async_db import async_db as db


class TagMixin:
    @staticmethod
    async def tag_list() -> List[Tag]:
        return await db.all(model=Tag)

    @staticmethod
    async def tag_get(tag_id: str) -> Tag:
        return await db.get(model=Tag, filters=[Tag.slug == tag_id])

    @classmethod
    async def tag_create(cls, request: TagCreateRequest) -> Tag:
        try:
            await cls.tag_get(tag_id=request.slug)
            raise errors.ObjectAlreadyExists(
                model=Tag, query={"name": request.name}
            )
        except errors.ObjectNotFound:
            tag = Tag.create(
                name=request.name, color=(request.color or RGB().hex),
            )
            return await db.save(tag)

    @classmethod
    async def tag_update(cls, tag_id: str, request: TagUpdateRequest,) -> Tag:
        tag = await cls.tag_get(tag_id=tag_id)
        # Change name
        if request.name is not None:
            tag.rename(request.name)
        # Change color
        if request.color is not None:
            tag.color = request.color

        return await db.update(tag)

    @classmethod
    async def tag_delete(cls, tag_id: str) -> bool:
        tag = await cls.tag_get(tag_id=tag_id)
        return await db.delete(obj=tag)
