from typing import List, Tuple
import datetime
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(user_id="1", email='teste@gmail.com', name='Gabriel Godoy', role=ROLE.ADMIN_COLLABORATOR, systems=["GAIA"], enabled=True, user_status=USER_STATUS.CONFIRMED, ttl=123),
            User(user_id="2", email='teste2@gmail.com', name='Gabriel Godoy', role=ROLE.COLLABORATOR, enabled=True, user_status=USER_STATUS.UNCONFIRMED, ttl=123),
            User(user_id="3",email='teste3@gmail.com', name='Gabriel Godoy', role=ROLE.USER, enabled=True, user_status=USER_STATUS.FORCE_CHANGE_PASSWORD, ttl=123),
        ]

        self.systems = ["GAIA", "JUNDIAI", "FORMULARIOS"]
    
    def get_user_by_access_token(self, access_token: str) -> User:
        pass
    
    def get_all_users(self) -> List[User]:
        return self.users

    def create_user(self, email: str, name: str, role: ROLE, systems: List[str]) -> User:
        for user in self.users:
            if user.email == email:
                raise DuplicatedItem("Usuário já cadastrado")
            
        for system in systems:
            if system not in self.systems:
                raise EntityError("systems")
        
        new_user = User(email=email, name=name, role=role, systems=systems, enabled=True, user_status=USER_STATUS.CONFIRMED, ttl=123)
        new_user.user_id = str(len(self.users) + 1)
        self.users.append(new_user)
        return self.get_user_by_email(new_user.email)
    
    def get_user_by_email(self, email: str) -> User:
        for userx in self.users:
            if userx.email == email:
                return userx
        return None
    
    def get_users_in_system(self, system: str) -> List[User]:
        users: List[User] = []
        for user in self.users:
            if system in user.systems:
                users.append(user)
        return users
    
    def update_user(self, user_email: str, kvp_to_update: dict, addSystems: List[str] = None, removeSystems: List[str] = None, enabled: bool = None) -> User:

        for idx, userx in enumerate(self.users):
            if userx.email == user_email:
                for key, value in kvp_to_update.items():
                    setattr(userx, key, value)
                if addSystems is not None:
                    for system in addSystems:
                        if system not in self.systems:
                            raise EntityError("systems")
                        userx.systems.append(system)
                
                if removeSystems is not None:
                    for system in removeSystems:
                        if system not in userx.systems:
                            raise EntityError("systems")
                        userx.systems.remove(system)
                
                if enabled is not None:
                    userx.enabled = enabled
                
                if type(userx.role) == str:
                    userx.role = ROLE[userx.role]

                return userx

        return None

    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        split_token = refresh_token.split("-")  # token, email
        if len(split_token) != 2:
            return None, None
        if split_token[0] != "valid_refresh_token":
            return None, None
        if self.get_user_by_email(split_token[1]) is None:
            return None, None
        tokens = "valid_access_token-" + split_token[1], refresh_token, "valid_id_token-" + split_token[1]
        return tokens