import pytest
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserUsecase:
    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        user_response = usecase(new_user_data={
                'name': 'Gabriel Godoy 01',
                'role': 'USER',
            }, user_email='teste@gmail.com', systems=["GAIA", "JUNDIAI"], enabled=False, requester_role=ROLE.ADMIN_COLLABORATOR)
        
        assert user_response.email == 'teste@gmail.com'
        assert user_response.role == ROLE.USER
        assert user_response.systems == ["GAIA", "JUNDIAI"]
        assert user_response.name == 'Gabriel Godoy 01'
        assert user_response.enabled == False
    
    def test_update_user_usecase_user_not_allowed(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(new_user_data={
                    'name': 'Gabriel Godoy 01',
                    'role': 'USER',
            }, user_email='teste@gmail.com', systems=["GAIA", "JUNDIAI"], enabled=False, requester_role=ROLE.ADMIN_USER)
    
    def test_update_user_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)

        with pytest.raises(NoItemsFound):
            usecase(new_user_data={
                    'name': 'Gabriel Godoy 01',
                    'role': 'USER',
            }, user_email='invalid', systems=["GAIA", "JUNDIAI"], enabled=False, requester_role=ROLE.ADMIN_COLLABORATOR)



