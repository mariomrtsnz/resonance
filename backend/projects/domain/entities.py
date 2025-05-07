from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DomainProject:
    owner_id: UUID 
    title: str
    
    id: UUID = field(default_factory=uuid4)
    description: str = ""
    needed_skill_text: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
