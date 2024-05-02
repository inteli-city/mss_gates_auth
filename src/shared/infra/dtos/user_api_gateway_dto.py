from typing import List
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE


class UserApiGatewayDTO:
    name: str
    email: str
    user_id: str
    role: ROLE
    groups: List[GROUPS]

    def __init__(self, name: str, email:str, user_id: str, role: ROLE, groups: List[GROUPS] = []):
        self.name = name
        self.email = email
        self.user_id = user_id
        self.role = role
        self.groups = groups

    @staticmethod
    def from_api_gateway(user_data: dict) -> 'UserApiGatewayDTO':
        """
        This method is used to convert the user data from the API Gateway to a UserApiGatewayDTO object.
        """
        return UserApiGatewayDTO(
            name=user_data['name'],
            email=user_data['email'],
            user_id=user_data['sub'],
            role=ROLE[user_data['custom:general_role']],
            groups=[GROUPS[group.strip()] for group in user_data.get('cognito:groups', '').split(',') if group.strip()]
        )
    
    def __eq__(self, other):
        return self.name == other.name and self.email == other.email and self.user_id == other.user_id and self.role == other.role and self.groups == other.groups