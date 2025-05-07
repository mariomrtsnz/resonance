from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from .entities import Skill

class AbstractSkillRepository(ABC):
    @abstractmethod
    def add(self, skill: Skill) -> Skill:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, skill_id: int) -> Optional[Skill]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Skill]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Skill]:
        raise NotImplementedError

    @abstractmethod
    def update(self, skill: Skill) -> Skill:
        raise NotImplementedError

    @abstractmethod
    def delete(self, skill_id: int) -> None:
        raise NotImplementedError