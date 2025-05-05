from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class UserRegistrationDTO:
    email: str
    password: str 

@dataclass(frozen=True)
class UserDTO:
    id: uuid.UUID
    email: str
    username: str 