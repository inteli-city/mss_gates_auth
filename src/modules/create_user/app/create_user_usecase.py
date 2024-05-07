from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class CreateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, email: str, name: str, role: ROLE, groups: list, requester_role: ROLE) -> User:
        
        if requester_role != ROLE.ADMIN_COLLABORATOR and requester_role != ROLE.ADMIN_USER:
            raise ForbiddenAction("Usuário não tem permissão para criar usuários")
        
        user_response = self.repo.create_user(email=email, name=name, role=role, groups=groups)

        return user_response
