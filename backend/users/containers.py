from dependency_injector import containers, providers

from users.application.services import UserService
from users.domain.repositories import AbstractUserRepository
from users.infrastructure.persistence.repositories import DjangoUserRepository

class UserContainer(containers.DeclarativeContainer):
    """Dependency Injection container for the users module."""

    # Configuration (can be loaded from settings or environment)
    # config = providers.Configuration()

    user_repository: providers.Factory[AbstractUserRepository] = providers.Factory(
        DjangoUserRepository
    )

    user_service: providers.Factory[UserService] = providers.Factory(
        UserService,
        user_repository=user_repository,
    ) 