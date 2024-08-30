import pytest
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUseUsecase:

    def test_create_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        
        user_response = usecase(email='teste@gmail3.com', name='Gabriel Godoy', role=ROLE.ADMIN_COLLABORATOR, systems=["GAIA"], requester_role=ROLE.ADMIN_COLLABORATOR)

        assert user_response.role == ROLE.ADMIN_COLLABORATOR
        assert user_response.email == 'teste@gmail3.com'
        assert user_response.name == 'Gabriel Godoy'
        assert user_response.systems == ["GAIA"]
        assert user_response.enabled == True
        assert user_response.user_status == USER_STATUS.CONFIRMED
    
    def test_create_user_usecase_user_not_allowed(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
    
        with pytest.raises(ForbiddenAction):
            usecase(email='teste@gmail.com', name='Gabriel Godoy', role=ROLE.COLLABORATOR, systems=["GAIA"], requester_role=ROLE.USER)

        