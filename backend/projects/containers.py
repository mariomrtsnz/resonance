from dependency_injector import containers, providers

from projects.application.services import ProjectService
from projects.infrastructure.persistence.repositories import DjangoProjectRepository
from projects.domain.repositories import AbstractProjectRepository

class ProjectContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    project_repository: providers.Provider[AbstractProjectRepository] = providers.Singleton(
        DjangoProjectRepository
    )

    project_service = providers.Factory(
        ProjectService,
        repository=project_repository,
    ) 