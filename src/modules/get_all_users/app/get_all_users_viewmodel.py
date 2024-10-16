from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS

class UserViewmodel:
    user_id: str
    name: str
    email: str
    role: ROLE
    systems: List[str]
    enabled: bool
    user_status: USER_STATUS
    ttl: int

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.role = user.role
        self.systems = user.systems
        self.enabled = user.enabled
        self.user_status = user.user_status
        self.ttl = user.ttl

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'role': self.role.value,
            'systems': self.systems,
            'enabled': self.enabled,
            'user_status': self.user_status.value,
            'ttl': self.ttl
        }

class GetAllUsersViewmodel:
    users: List[UserViewmodel]

    def __init__(self, users: List[User]):
        self.users = [UserViewmodel(user).to_dict() for user in users]

    def to_dict(self):
        return {
            'users': self.users,
            'message': 'Usuários foram listados com sucesso!'
        }