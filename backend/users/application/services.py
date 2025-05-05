import uuid
from typing import Optional, Dict, Any

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from users.domain.entities import User as DomainUser 
from users.domain.repositories import AbstractUserRepository

class UserRegistrationError(Exception):
    pass

class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self._user_repository = user_repository

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[DomainUser]:
        return self._user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[DomainUser]:
        return self._user_repository.get_by_email(email)

    def register_user(self, registration_data: Dict[str, Any]) -> DomainUser:
        email = registration_data['email']
        password = registration_data['password']

        if self._user_repository.get_by_email(email):
            raise UserRegistrationError(f"User with email {email} already exists.")

        hashed_password = make_password(password)

        user = DomainUser(
            username=email,
            email=email,
        )
        
        try:
            created_user = self._user_repository.add(user, hashed_password)
            return created_user
        except IntegrityError as e:
            raise UserRegistrationError(f"Database error during registration: {e}")
        except Exception as e:
            # TODO: Add proper logging here
            raise UserRegistrationError(f"An unexpected error occurred: {e}")
