import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class CollaborationStatus(Enum):
    OPEN_TO_HELP = 'OPEN'
    NEEDS_HELP = 'NEEDS'
    NOT_LOOKING = 'NONE'

@dataclass
class User:
    username: str
    email: str
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_staff: bool = False
    date_joined: datetime = field(default_factory=datetime.now)

    bio: str = ""
    location: str = ""
    collaboration_status: CollaborationStatus = CollaborationStatus.NOT_LOOKING
