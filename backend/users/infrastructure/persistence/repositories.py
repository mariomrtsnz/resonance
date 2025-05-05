import uuid
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from users.domain.entities import User as DomainUser, CollaborationStatus
from users.domain.repositories import AbstractUserRepository
from .models import User as OrmUser, UserProfile

def _to_domain_user(orm_user: OrmUser) -> DomainUser:
    profile_bio = getattr(orm_user.profile, 'bio', '')
    profile_location = getattr(orm_user.profile, 'location', '')
    profile_status_str = getattr(orm_user.profile, 'collaboration_status', CollaborationStatus.NOT_LOOKING.value)
    
    return DomainUser(
        id=orm_user.id,
        username=orm_user.username,
        email=orm_user.email,
        first_name=orm_user.first_name,
        last_name=orm_user.last_name,
        is_active=orm_user.is_active,
        is_staff=orm_user.is_staff,
        date_joined=orm_user.date_joined,
        bio=profile_bio,
        location=profile_location,
        collaboration_status=CollaborationStatus(profile_status_str) 
    )

def _to_orm_user_and_profile(domain_user: DomainUser) -> tuple[OrmUser, UserProfile]:
    orm_user_data = {
        'username': domain_user.username,
        'email': domain_user.email,
        'first_name': domain_user.first_name,
        'last_name': domain_user.last_name,
        'is_active': domain_user.is_active,
        'is_staff': domain_user.is_staff,
    }

    if domain_user.id:
        orm_user_data['id'] = domain_user.id

    orm_user = OrmUser(**orm_user_data)

    profile_data = {
        'bio': domain_user.bio,
        'location': domain_user.location,
        'collaboration_status': domain_user.collaboration_status.value,
    }
    orm_profile = UserProfile(**profile_data)

    return orm_user, orm_profile


class DjangoUserRepository(AbstractUserRepository):
    def get_by_id(self, user_id: uuid.UUID) -> Optional[DomainUser]:
        try:
            orm_user = OrmUser.objects.select_related('profile').get(id=user_id)
            return _to_domain_user(orm_user)
        except ObjectDoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        try:
            orm_user = OrmUser.objects.select_related('profile').get(email=email)
            return _to_domain_user(orm_user)
        except ObjectDoesNotExist:
            return None

    @transaction.atomic
    def add(self, user: DomainUser, password_hash: str) -> DomainUser:
        orm_user, orm_profile = _to_orm_user_and_profile(user)
        
        orm_user.password = password_hash
        
        if not orm_user.email:
             raise ValueError("Email cannot be empty.")
        if not orm_user.username:
            orm_user.username = orm_user.email

        orm_user.save()
        orm_profile.user = orm_user
        orm_profile.save()
        
        created_orm_user = OrmUser.objects.select_related('profile').get(id=orm_user.id)
        return _to_domain_user(created_orm_user) 

    @transaction.atomic
    def update(self, user: DomainUser) -> None:
        if not user.id:
             raise ValueError("Cannot update a user without an ID.")
             
        orm_user_data, orm_profile_data_obj = _to_orm_user_and_profile(user)
        
        try:
            existing_user = OrmUser.objects.select_related('profile').get(id=user.id)
        except OrmUser.DoesNotExist:
             raise ValueError(f"User with ID {user.id} not found for update.")
        
        for field, value in orm_user_data.__dict__.items():
            if field not in ['id', 'password', 'date_joined', 'last_login']:
                 setattr(existing_user, field, value)
        existing_user.save()

        existing_profile = existing_user.profile
        for field, value in orm_profile_data_obj.__dict__.items():
             if field not in ['_state', 'id', 'user_id']:
                 setattr(existing_profile, field, value)
        existing_profile.save()
