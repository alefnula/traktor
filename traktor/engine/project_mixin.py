from typing import List, Optional

from django_tea import errors

from traktor.models import Project


class ProjectMixin:
    @staticmethod
    def project_list() -> List[Project]:
        return list(Project.objects.all())

    @staticmethod
    def project_get(project_id: str) -> Project:
        try:
            return Project.get_by_slug(slug=project_id)
        except Project.DoesNotExist:
            raise errors.ObjectNotFound(
                model=Project, query={"project_id": project_id}
            )

    @classmethod
    def project_create(cls, name: str, color: Optional[str] = None) -> Project:
        try:
            Project.get_by_slug_field(value=name)
            raise errors.ObjectAlreadyExists(
                model=Project, query={"name": name}
            )
        except Project.DoesNotExist:
            return Project.objects.create(
                name=name, color=color or Project.color.field.default
            )

    @classmethod
    def project_update(
        cls, project_id: str, name: Optional[str], color: Optional[str],
    ) -> Project:
        project = cls.project_get(project_id=project_id)
        # Change name
        if name is not None:
            project.name = name
        # Change color
        if color is not None:
            project.color = color
        project.save()
        return project

    @classmethod
    def project_delete(cls, project_id: str):
        project = cls.project_get(project_id=project_id)
        project.delete()
