from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from ..domain.entities import DomainProject as DomainProject
@dataclass(frozen=True)
class ProjectCreateDTO:
    title: str
    description: Optional[str] = None
    needed_skill_text: Optional[str] = None

@dataclass(frozen=True)
class ProjectDTO:
    id: UUID
    owner_id: UUID
    title: str
    description: Optional[str]
    needed_skill_text: Optional[str]
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: DomainProject) -> 'ProjectDTO':
        return cls(
            id=entity.id,
            owner_id=entity.owner_id,
            title=entity.title,
            description=entity.description,
            needed_skill_text=entity.needed_skill_text,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat()
        )