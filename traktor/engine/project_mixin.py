from typing import List, Optional

from tea_django import errors

from traktor.models import User, Project


class ProjectMixin:
    @staticmethod
    def project_list(user: User) -> List[Project]:
        return list(Project.objects.filter(user=user))

    @staticmethod
    def project_get(user: User, project_id: str) -> Project:
        try:
            return Project.get_by_slug(slug=project_id, user=user)
        except Project.DoesNotExist:
            raise errors.ObjectNotFound(
                model=Project,
                query={"user": user.username, "project_id": project_id},
            )

    @classmethod
    def project_create(
        cls, user: User, name: str, color: Optional[str] = None
    ) -> Project:
        try:
            Project.get_by_slug_field(value=name, user=user)
            raise errors.ObjectAlreadyExists(
                model=Project, query={"user": user.username, "name": name}
            )
        except Project.DoesNotExist:
            return Project.objects.create(
                user=user,
                name=name,
                color=color or Project.color.field.default,
            )

    @classmethod
    def project_update(
        cls,
        user: User,
        project_id: str,
        name: Optional[str],
        color: Optional[str],
    ) -> Project:
        project = cls.project_get(user=user, project_id=project_id)
        # Change name
        if name is not None:
            project.name = name
        # Change color
        if color is not None:
            project.color = color
        project.save()
        return project

    @classmethod
    def project_delete(cls, user: User, project_id: str):
        project = cls.project_get(user=user, project_id=project_id)
        project.delete()
