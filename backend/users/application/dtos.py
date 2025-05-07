from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class UserRegistrationDTO:
    email: str
    password: str 

@dataclass(frozen=True)
class UserDTO:
    id: UUID
    email: str
    username: str 