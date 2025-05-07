from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from ..domain.entities import Skill as DomainSkill

@dataclass(frozen=True)
class SkillDTO:
    id: UUID
    name: str

    @classmethod
    def from_entity(cls, entity: DomainSkill) -> 'SkillDTO':
        return cls(id=entity.id, name=entity.name)

@dataclass(frozen=True)
class SkillCreateDTO:
    name: str

@dataclass(frozen=True)
class SkillUpdateDTO:
    name: str