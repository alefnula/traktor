from uuid import UUID
from typing import List

from traktor import errors
from traktor.models import RGB, Project
from traktor.db.async_db import async_db as db
from traktor.engine.async_engine.requests import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)


class ProjectMixin:
    @staticmethod
    async def project_list() -> List[Project]:
        return await db.all(model=Project)

    @staticmethod
    async def project_get(project_id: str) -> Project:
        try:
            UUID(project_id)
            return await db.get_by_id(model=Project, obj_id=project_id)
        except ValueError:
            return await db.get(
                model=Project, filters=[Project.name == project_id]
            )

    @classmethod
    async def project_create(cls, request: ProjectCreateRequest) -> Project:
        try:
            await cls.project_get(project_id=request.name)
            raise errors.ObjectAlreadyExists(
                model=Project, query={"name": request.name}
            )
        except errors.ObjectNotFound:
            project = Project.create(
                name=request.name, color_hex=(request.color or RGB().hex),
            )
            project = await db.save(project)
            return project

    @classmethod
    async def project_update(
        cls, project_id: str, request: ProjectUpdateRequest,
    ) -> Project:
        project = await cls.project_get(project_id=project_id)
        # Change name
        if request.name is not None:
            project.name = request.name
        # Change color
        if request.color is not None:
            project.color_hex = request.color

        await db.update(project)
        return project

    @classmethod
    async def project_delete(cls, project_id: str) -> bool:
        project = await cls.project_get(project_id=project_id)
        return await db.delete(obj=project)
