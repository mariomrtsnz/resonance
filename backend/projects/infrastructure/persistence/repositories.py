import uuid
from typing import Optional, List

from ...domain.entities import Project as ProjectEntity
from ...domain.repositories import AbstractProjectRepository
from .models import Project as ProjectModel
from django.db import transaction


class DjangoProjectRepository(AbstractProjectRepository):
    def get_by_id(self, project_id: uuid.UUID) -> Optional[ProjectEntity]:
        try:
            project_orm = ProjectModel.objects.select_related('owner').get(id=project_id)
            return self._to_entity(project_orm)
        except ProjectModel.DoesNotExist:
            return None

    @transaction.atomic
    def add(self, project: ProjectEntity) -> ProjectEntity:
        project_orm = ProjectModel.objects.create(
            id=project.id,
            owner_id=project.owner_id,
            title=project.title,
            description=project.description,
            needed_skill_text=project.needed_skill_text,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
        project_orm.refresh_from_db()
        return self._to_entity(project_orm)

    @transaction.atomic
    def update(self, project: ProjectEntity) -> None:
        ProjectModel.objects.filter(id=project.id).update(
            title=project.title,
            description=project.description,
            needed_skill_text=project.needed_skill_text,
            updated_at=project.updated_at
        )

    def list_by_owner(self, owner_id: uuid.UUID) -> List[ProjectEntity]:
        projects_orm = ProjectModel.objects.select_related('owner').filter(owner_id=owner_id)
        return [self._to_entity(p) for p in projects_orm]

    def get_all(self) -> List[ProjectEntity]:
        projects_orm = ProjectModel.objects.all().order_by("-created_at")
        return [self._to_entity(p) for p in projects_orm]

    def _to_entity(self, project_orm: ProjectModel) -> ProjectEntity:
        return ProjectEntity(
            id=project_orm.id,
            owner_id=project_orm.owner.id,
            title=project_orm.title,
            description=project_orm.description,
            needed_skill_text=project_orm.needed_skill_text,
            created_at=project_orm.created_at,
            updated_at=project_orm.updated_at
        ) 