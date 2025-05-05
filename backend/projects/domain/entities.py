import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Project:
    owner_id: uuid.UUID 
    title: str
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    description: str = ""
    needed_skill_text: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
