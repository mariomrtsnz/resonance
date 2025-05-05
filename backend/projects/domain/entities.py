import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Project:
    """Domain entity representing a Project. Framework-agnostic."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    owner_id: uuid.UUID
    title: str
    description: str = ""
    needed_skill_text: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
