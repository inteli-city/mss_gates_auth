from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class RefreshTokenUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo
    
    def __call__(self, refresh_token: str) -> str:
        tokens = self.repo.refresh_token(refresh_token)

        if tokens is None or tokens == (None, None):
            raise ForbiddenAction(f'Refresh Token')

        access_token, refresh_token, id_token = tokens
        
        return access_token, refresh_token, id_token