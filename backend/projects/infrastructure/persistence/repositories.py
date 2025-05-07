from django.db import transaction
from typing import Optional, List
from uuid import UUID

from ...domain.exceptions import ProjectNotFoundError
from ...domain.entities import DomainProject
from ...domain.repositories import AbstractProjectRepository
from .models import Project as ProjectModel

def _to_domain_entity(project_orm: ProjectModel) -> DomainProject:
    return DomainProject(
        id=project_orm.id,
        owner_id=project_orm.owner.id,
        title=project_orm.title,
        description=project_orm.description,
        needed_skill_text=project_orm.needed_skill_text,
        created_at=project_orm.created_at,
        updated_at=project_orm.updated_at
    )
class DjangoProjectRepository(AbstractProjectRepository):

    
    def get_by_id(self, project_id: UUID) -> Optional[DomainProject]:
        try:
            project_orm = ProjectModel.objects.select_related('owner').get(id=project_id)
            return _to_domain_entity(project_orm)
        except ProjectModel.DoesNotExist:
            raise ProjectNotFoundError(identifier=project_id)

    @transaction.atomic
    def add(self, project: DomainProject) -> DomainProject:
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
        return _to_domain_entity(project_orm)

    @transaction.atomic
    def update(self, project: DomainProject) -> None:
        ProjectModel.objects.filter(id=project.id).update(
            title=project.title,
            description=project.description,
            needed_skill_text=project.needed_skill_text,
            updated_at=project.updated_at
        )

    def list_by_owner(self, owner_id: UUID) -> List[DomainProject]:
        projects_orm = ProjectModel.objects.select_related('owner').filter(owner_id=owner_id)
        return [_to_domain_entity(p) for p in projects_orm]

    def get_all(self) -> List[DomainProject]:
        projects_orm = ProjectModel.objects.all().order_by("-created_at")
        return [_to_domain_entity(p) for p in projects_orm]
