from abc import ABC, abstractmethod
import uuid
from typing import Optional, List

from .entities import Project

class AbstractProjectRepository(ABC):
    @abstractmethod
    def get_by_id(self, project_id: uuid.UUID) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    def add(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def update(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_owner(self, owner_id: uuid.UUID) -> List[Project]:
        raise NotImplementedError
