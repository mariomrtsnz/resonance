from ..domain.entities import Project
from ..domain.repositories import AbstractProjectRepository
from .dtos import ProjectCreateDTO, ProjectDTO
from typing import List
from uuid import UUID
from ..domain.exceptions import ProjectNotFoundError

class ProjectService:
    def __init__(self, repository: AbstractProjectRepository):
        self._repository = repository

    def get_all_projects(self) -> List[ProjectDTO]:
        projects = self._repository.get_all()
        return [ProjectDTO.from_entity(p) for p in projects]

    def create_project(self, project_data: ProjectCreateDTO, owner_id: UUID) -> ProjectDTO:
        description = project_data.description if project_data.description != '' else None
        needed_skill_text = project_data.needed_skill_text if project_data.needed_skill_text != '' else None

        project_entity = Project(
            owner_id=owner_id,
            title=project_data.title,
            description=description,
            needed_skill_text=needed_skill_text
        )
        
        created_project = self._repository.add(project_entity)

        return ProjectDTO.from_entity(created_project)
    
    def get_project_by_id(self, project_id: UUID) -> ProjectDTO:
        project = self._repository.get_by_id(project_id)

        if not project:
            raise ProjectNotFoundError(f"Project with id {project_id} not found")
        
        return ProjectDTO.from_entity(project)
