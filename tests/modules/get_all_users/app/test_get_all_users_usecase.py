import pytest
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersUsecase:

    def test_get_all_users_usecase(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)
        users_response = usecase(requester_role=ROLE.COLLABORATOR)

        assert len(users_response) == 3
    
    def test_get_all_users_usecase_user_not_allowed(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(requester_role=ROLE.ADMIN)