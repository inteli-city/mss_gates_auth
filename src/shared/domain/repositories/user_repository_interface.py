from abc import ABC, abstractmethod
from typing import List, Tuple

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class IUserRepository(ABC):

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, email: str, name: str, role: ROLE, systems: List[str]) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def get_users_in_system(self, system: str) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user_email: str, kvp_to_update: dict, addSystems: List[str] = None, removeSystems: List[str] = None, enabled: bool = None) -> User:
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        pass
