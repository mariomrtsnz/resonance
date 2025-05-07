from dependency_injector import containers, providers

from .application.services import SkillService
from .infrastructure.persistence.repositories import DjangoSkillRepository
from .domain.repositories import AbstractSkillRepository

class SkillContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    skill_repository: providers.Provider[AbstractSkillRepository] = providers.Singleton(
        DjangoSkillRepository
    )

    skill_service = providers.Factory(
        SkillService,
        repository=skill_repository,
    ) 