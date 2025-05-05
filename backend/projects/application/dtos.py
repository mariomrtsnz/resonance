import uuid
from dataclasses import dataclass

@dataclass(frozen=True)
class ProjectCreateDTO:
    owner_id: uuid.UUID
    title: str
    description: str
    needed_skill_text: str

@dataclass(frozen=True)
class ProjectDTO:
    id: uuid.UUID
    owner_id: uuid.UUID
    title: str
    description: str
    needed_skill_text: str
    created_at: str 
    updated_at: str