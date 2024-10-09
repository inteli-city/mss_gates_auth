from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo
    
    def __call__(self, access_token: str):
        user = self.repo.get_user_by_access_token(access_token=access_token)

        if user is None:
            raise NoItemsFound("Usuário não encontrado")

        return user