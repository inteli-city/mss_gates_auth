from typing import List, Tuple

from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class UserRepositoryMock(IUserRepository):
    users: List[User]

    def __init__(self):
        self.users = [
            User(user_id="1", email='teste@gmail.com', name='Gabriel Godoy', role=ROLE.ADMIN_COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED),
            User(user_id="2", email='teste2@gmail.com', name='Gabriel Godoy', role=ROLE.COLLABORATOR, enabled=True, user_status=USER_STATUS.UNCONFIRMED),
            User(user_id="3",email='teste3@gmail.com', name='Gabriel Godoy', role=ROLE.USER, enabled=True, user_status=USER_STATUS.FORCE_CHANGE_PASSWORD),
        ]
    
    def get_all_users(self) -> List[User]:
        return self.users

    def create_user(self, email: str, name: str, role: ROLE, groups: List[GROUPS]) -> User:
        new_user = User(email=email, name=name, role=role, groups=groups, enabled=True, user_status=USER_STATUS.CONFIRMED)
        new_user.user_id = str(len(self.users) + 1)
        self.users.append(new_user)
        return self.get_user_by_email(new_user.email)
    
    def get_user_by_email(self, email: str) -> User:
        for userx in self.users:
            if userx.email == email:
                return userx
                
        return None
    
    def get_users_in_group(self, group: GROUPS) -> List[User]:
        users: List[User] = []
        for user in self.users:
            if group in user.groups:
                users.append(user)
        return users
    
    def update_user(self, user_email: str, kvp_to_update: dict, addGroups: List[GROUPS] = None, removeGroups: List[GROUPS] = None, enabled: bool = None) -> User:
        for idx, userx in enumerate(self.users):
            if userx.email == user_email:
                for key, value in kvp_to_update.items():
                    setattr(userx, key, value)
                if addGroups is not None:
                    for group in addGroups:
                        userx.groups.append(group)
                
                if removeGroups is not None:
                    for group in removeGroups:
                        userx.groups.remove(group)
                
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