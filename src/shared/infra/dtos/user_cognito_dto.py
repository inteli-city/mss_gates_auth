from enum import Enum
from typing import List, Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class UserCognitoDTO:
    user_id: str
    name: str
    email: str
    role: ROLE
    groups: List[GROUPS]
    enabled: bool
    user_status: USER_STATUS

    def __init__(self, user_id: str, email: str, name: str, role: ROLE, enabled: bool, user_status: USER_STATUS, groups: List[GROUPS] = []):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.groups = groups
        self.enabled = enabled
        self.user_status = user_status

    @staticmethod
    def from_entity(user: User):
        return UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            role=user.role,
            groups=user.groups,
            enabled=user.enabled,
            user_status=user.user_status
        )

    TO_COGNITO_DICT = {
        "email": "email",
        "name": "name",
        "role": "custom:general_role",
    }

    FROM_COGNITO_DICT = {value: key for key, value in TO_COGNITO_DICT.items()}
    FROM_COGNITO_DICT["sub"] = "user_id"

    def to_cognito_attributes(self) -> List[dict]:
        user_attributes = []
        for att, name in self.TO_COGNITO_DICT.items():
            value = getattr(self, att)
            if isinstance(value, Enum):  # Verifica se é um enum
                value = value.value  # Obtém o valor do enum
            user_attributes.append(self.parse_attribute(value=value, name=name))
        
        user_attributes = [att for att in user_attributes if att["Value"] != str(None)]

        return user_attributes
    
    @staticmethod
    def from_cognito(data: dict) -> "UserCognitoDTO":
        user_data = next((value for key, value in data.items() if "Attribute" in key), None)
        user_data = {UserCognitoDTO.FROM_COGNITO_DICT[att["Name"]]: att["Value"] for att in user_data if att["Name"] in UserCognitoDTO.FROM_COGNITO_DICT}
        # user_data["created_at"] = data.get("UserCreateDate")
        # user_data["updated_at"] = data.get("UserLastModifiedDate")
        user_data["enabled"] = f'{data.get("Enabled")}'
        user_data["status"] = f'{data.get("UserStatus")}'

        return UserCognitoDTO(
            user_id=str(user_data["user_id"]),
            email=str(user_data["email"]),
            name=str(user_data["name"]),
            role = ROLE[user_data["role"]],
            enabled=bool(user_data.get("enabled").lower() == "true"),
            user_status=USER_STATUS[user_data["status"]],
        )

    def to_entity(self) -> User:
        return User(
            user_id=self.user_id,
            email=self.email,
            name=self.name,
            role=self.role,
            groups=self.groups,
            enabled=self.enabled,
            user_status=self.user_status
        )
    
    @staticmethod
    def parse_attribute(name, value) -> dict:
        return {'Name': name, 'Value': str(value)}


