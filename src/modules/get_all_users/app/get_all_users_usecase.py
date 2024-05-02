from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class GetAllUsersUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, requester_role: ROLE) -> List[User]:

        if requester_role != ROLE.COLLABORATOR:
            raise ForbiddenAction("Usuário não tem permissão para criar usuários")
        
        users_response = self.repo.get_all_users()

        return users_response