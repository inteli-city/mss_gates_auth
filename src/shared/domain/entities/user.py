import abc
import re
from typing import List
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.errors.domain_errors import EntityError


class User(abc.ABC):
    user_id: str = None
    name: str
    email: str
    role: ROLE
    systems: List[str]
    enabled: bool
    user_status: USER_STATUS
    ttl: int # time to live - timestamp
    MIN_NAME_LENGTH = 2

    def __init__(self, name: str, email: str, role: ROLE, enabled: bool, user_status: USER_STATUS, ttl: int, systems: List[str] = [], user_id: str = None):
        if type(user_id) != str and user_id is not None:
            raise EntityError("user_id")
        self.user_id = user_id
        
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if type(role) != ROLE:
            raise EntityError("role")
        self.role = role

        if type(systems) != list:
            raise EntityError("systems")
        self.systems = systems

        if type(enabled) != bool:
            raise EntityError("enabled")
        self.enabled = enabled

        if type(user_status) != USER_STATUS:
            raise EntityError("user_status")
        self.user_status = user_status

        if type(ttl) != int:
            raise EntityError("ttl")
        self.ttl = ttl

    @staticmethod
    def parse_object(user: dict) -> 'User':
        return User(
            user_id=user['user_id'] if 'user_id' in user else None,
            email=user['email'],
            name=user['name'].title(),
            role=ROLE[user['role']],
            systems=user['systems'],
            enabled=user['enabled'],
            user_status=USER_STATUS[user['user_status']],
            ttl=user['ttl']
        )

    @staticmethod
    def validate_name(name: str) -> bool:
        if name is None:
            return False
        elif type(name) != str:
            return False
        elif len(name) < User.MIN_NAME_LENGTH:
            return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        if email is None:
            return False
        elif type(email) != str:
            return False
        
        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

        return bool(re.fullmatch(regex, email))

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'role': self.role.value,
            'systems': self.systems,
            'enabled': self.enabled,
            'user_status': self.user_status.value,
            'ttl': self.ttl
        }

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.name}, email={self.email}, role={self.role}, systems={self.systems}, enabled={self.enabled}, user_status={self.user_status}, ttl={self.ttl})"
