from abc import ABC, abstractmethod
import uuid
from typing import Optional, List

from .entities import DomainProject

class AbstractProjectRepository(ABC):
    @abstractmethod
    def get_by_id(self, project_id: uuid.UUID) -> Optional[DomainProject]:
        raise NotImplementedError

    @abstractmethod
    def add(self, project: DomainProject) -> DomainProject:
        raise NotImplementedError

    @abstractmethod
    def update(self, project: DomainProject) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_owner(self, owner_id: uuid.UUID) -> List[DomainProject]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[DomainProject]:
        raise NotImplementedError
