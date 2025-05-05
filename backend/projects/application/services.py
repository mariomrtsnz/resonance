from ..domain.entities import Project
from ..domain.repositories import AbstractProjectRepository
from .dtos import ProjectCreateDTO, ProjectDTO

class ProjectService:
    def __init__(self, repository: AbstractProjectRepository):
        self._repository = repository

    def create_project(self, data: ProjectCreateDTO) -> ProjectDTO:
        project_entity = Project(
            owner_id=data.owner_id,
            title=data.title,
            description=data.description,
            needed_skill_text=data.needed_skill_text
        )
        
        created_project = self._repository.add(project_entity)

        return ProjectDTO(
            id=created_project.id,
            owner_id=created_project.owner_id,
            title=created_project.title,
            description=created_project.description,
            needed_skill_text=created_project.needed_skill_text,
            created_at=created_project.created_at.isoformat(),
            updated_at=created_project.updated_at.isoformat(),
        ) 