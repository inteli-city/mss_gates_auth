from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class ListUsersInGroupUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, group: GROUPS, request_user_role: ROLE, request_user_groups: List[GROUPS]) -> List[User]:
        
        if request_user_role != ROLE.COLLABORATOR and request_user_role != ROLE.ADMIN:
            raise ForbiddenAction("Usuário não tem permissão para buscar usuários em grupos")               

        if group not in request_user_groups:
            raise ForbiddenAction("Usuário não tem permissão para buscar usuários deste grupo")

        users_response = self.repo.get_users_in_group(group=group)

        return users_response