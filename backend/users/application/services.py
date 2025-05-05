import uuid
from typing import Optional

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from .dtos import UserRegistrationDTO, UserDTO
from users.domain.entities import User as DomainUser 
from users.domain.repositories import AbstractUserRepository

class UserRegistrationError(Exception):
    pass

class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self._user_repository = user_repository

    def _map_domain_user_to_dto(self, user: DomainUser) -> UserDTO:
        return UserDTO(id=user.id, email=user.email, username=user.username)

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[UserDTO]:
        user = self._user_repository.get_by_id(user_id)
        return self._map_domain_user_to_dto(user) if user else None

    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        user = self._user_repository.get_by_email(email)
        return self._map_domain_user_to_dto(user) if user else None

    def register_user(self, registration_dto: UserRegistrationDTO) -> UserDTO:
        email = registration_dto.email
        password = registration_dto.password

        if self._user_repository.get_by_email(email):
            raise UserRegistrationError(f"User with email {email} already exists.")

        hashed_password = make_password(password)

        domain_user_entity = DomainUser(
            username=email,
            email=email,
        )
        
        try:
            created_user = self._user_repository.add(domain_user_entity, hashed_password)
            return self._map_domain_user_to_dto(created_user)
        except IntegrityError as e:
            raise UserRegistrationError(f"Database error during registration: {e}")
        except Exception as e:
            # TODO: Add proper logging here
            raise UserRegistrationError(f"An unexpected error occurred: {e}")
