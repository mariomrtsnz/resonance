from ..domain.entities import Skill as DomainSkill
from ..domain.repositories import AbstractSkillRepository
from .dtos import SkillCreateDTO, SkillDTO, SkillUpdateDTO
from typing import List
from uuid import UUID
from ..domain.exceptions import SkillNotFoundError, SkillAlreadyExistsError

class SkillService:
    def __init__(self, repository: AbstractSkillRepository):
        self._repository = repository

    def get_all_skills(self) -> List[SkillDTO]:
        skills = self._repository.get_all()
        return [SkillDTO.from_entity(s) for s in skills]

    def create_skill(self, skill_dto: SkillCreateDTO) -> SkillDTO:
        existing_skill = self._repository.get_by_name(skill_dto.name)
        if existing_skill:
            raise SkillAlreadyExistsError(skill_dto.name)
        
        skill_entity = DomainSkill(name=skill_dto.name)
        
        created_skill = self._repository.add(skill_entity)
        
        return SkillDTO.from_entity(created_skill)
    
    def get_skill_by_id(self, skill_id: UUID) -> SkillDTO:
        skill = self._repository.get_by_id(skill_id)
        if not skill:
            raise SkillNotFoundError(skill_id)
        
        return SkillDTO.from_entity(skill)
    
    def update_skill(self, skill_id: UUID, skill_dto: SkillUpdateDTO) -> SkillDTO:
        skill_to_update = self._repository.get_by_id(skill_id)
        if not skill_to_update:
            raise SkillNotFoundError(skill_id)
        
        if skill_to_update.name != skill_dto.name:
            existing_skill_with_new_name = self._repository.get_by_name(skill_dto.name)
            if existing_skill_with_new_name and existing_skill_with_new_name.id != skill_id:
                raise SkillAlreadyExistsError(skill_dto.name)
            
        
        skill_to_update.name = skill_dto.name
        
        updated_skill = self._repository.update(skill_to_update)
        
        return SkillDTO.from_entity(updated_skill)
        
    def delete_skill(self, skill_id: UUID) -> None:
        skill_to_delete = self._repository.get_by_id(skill_id)
        if not skill_to_delete:
            raise SkillNotFoundError(skill_id)
        
        self._repository.delete(skill_id)

    def get_skill_by_name(self, name: str) -> SkillDTO:
        skill = self._repository.get_by_name(name)
        if not skill:
            raise SkillNotFoundError(name)
        
        return SkillDTO.from_entity(skill)
        