from django.db import transaction
from typing import Optional, List
from uuid import UUID

from ...domain.exceptions import SkillNotFoundError
from ...domain.entities import Skill as DomainSkill
from ...domain.repositories import AbstractSkillRepository
from .models import Skill as SkillModel

def _to_domain_entity(orm_skill: SkillModel) -> DomainSkill:
    return DomainSkill(
        id=orm_skill.id,
        name=orm_skill.name
    )

class DjangoSkillRepository(AbstractSkillRepository):

    def get_by_id(self, skill_id: UUID) -> Optional[DomainSkill]:
        try:
            skill_orm = SkillModel.objects.get(id=skill_id)
            return _to_domain_entity(skill_orm)
        except SkillModel.DoesNotExist:
            raise SkillNotFoundError(identifier=skill_id)
    
    def add(self, skill: DomainSkill) -> DomainSkill:
        skill_orm = SkillModel.objects.create(name=skill.name)
        return _to_domain_entity(skill_orm)
    
    def get_by_name(self, name: str) -> Optional[DomainSkill]:
        try:
            skill_orm = SkillModel.objects.get(name=name)
            return _to_domain_entity(skill_orm)
        except SkillModel.DoesNotExist:
            return None
    
    def get_all(self) -> List[DomainSkill]:
        skills_orm = SkillModel.objects.all().order_by("name")
        return [_to_domain_entity(s) for s in skills_orm]
    
    @transaction.atomic
    def update(self, skill: DomainSkill) -> DomainSkill:
        try:
            skill_orm = SkillModel.objects.get(id=skill.id)
            skill_orm.name = skill.name
            skill_orm.save(update_fields=["name"])
            return _to_domain_entity(skill_orm)
        except SkillModel.DoesNotExist:
            raise SkillNotFoundError(identifier=skill.id)
        
    @transaction.atomic
    def delete(self, skill_id: UUID) -> None:
        try:
            skill_orm = SkillModel.objects.get(id=skill_id)
            skill_orm.delete()
        except SkillModel.DoesNotExist:
            raise SkillNotFoundError(identifier=skill_id)
        