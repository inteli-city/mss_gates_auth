from typing import Tuple
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
import pytest


class Test_UserRepositoryMock:

    def test_get_all_users(self):
        repo = UserRepositoryMock()
        users = repo.get_all_users()

        assert len(users) == 3
        assert type(users[0]) == User
        assert users[0].email == 'teste@gmail.com'
        assert users[0].name == 'Gabriel Godoy'
        assert users[0].role == ROLE.ADMIN_COLLABORATOR
        assert users[0].systems == ["GAIA"]

    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email('teste@gmail.com')

        assert user.name == 'Gabriel Godoy'
        assert type(user) == User

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = repo.create_user(email='teste4@gmail.com', name='Gabriel Godoy', role=ROLE.COLLABORATOR, systems=[])

        assert len(repo.users) == 4
        assert type(user) == User
        assert repo.users[-1].user_id == '4'
        assert repo.users[-1].email == 'teste4@gmail.com'
        assert repo.users[-1].name == 'Gabriel Godoy'
        assert repo.users[-1].role == ROLE.COLLABORATOR
        assert repo.users[-1].systems == []
    
    def test_create_user_duplicated(self):
        repo = UserRepositoryMock()
        with pytest.raises(DuplicatedItem):
            repo.create_user(email='teste@gmail.com', name='Gabriel Godoy', role=ROLE.COLLABORATOR, systems=[])

    def test_get_users_in_system(self):
        repo = UserRepositoryMock()
        users = repo.get_users_in_system("GAIA")

        assert len(users) == 1
        assert type(users[0]) == User
        assert users[0].email == 'teste@gmail.com'
        assert users[0].name == 'Gabriel Godoy'
        assert users[0].role == ROLE.ADMIN_COLLABORATOR
        assert users[0].systems == ["GAIA"]
    
    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user(user_email='teste@gmail.com', kvp_to_update={'role': ROLE.USER}, addSystems=["JUNDIAI"], removeSystems=["GAIA"], enabled=False)

        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.role == ROLE.USER
        assert user.systems == ["JUNDIAI"]
        assert user.enabled == False
    
    def test_update_user_enabled_null(self):
        repo = UserRepositoryMock()
        user = repo.update_user(user_email='teste@gmail.com', kvp_to_update={'role': ROLE.USER}, addSystems=["JUNDIAI"], removeSystems=["GAIA"])

        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.role == ROLE.USER
        assert user.systems == ["JUNDIAI"]
        assert user.enabled == True
    
    def test_update_user_return_none(self):
        repo = UserRepositoryMock()
        response = repo.update_user(user_email='teste@gmail.', kvp_to_update={'role': ROLE.USER}, addSystems=["JUNDIAI"], removeSystems=["GAIA"], enabled=False)

        assert response == None
    
    def test_refresh_token(self):
        repo = UserRepositoryMock()
        response = repo.refresh_token(
            refresh_token="valid_refresh_token-teste@gmail.com")
        assert response[0] == 'valid_access_token-teste@gmail.com'
        assert response[1] == 'valid_refresh_token-teste@gmail.com'
        assert response[2] == 'valid_id_token-teste@gmail.com'
    
    def test_refresh_token_return_none(self):
        repo = UserRepositoryMock()
        response = repo.refresh_token(
            refresh_token="valid_refresh_tokenteste@gmail.com")
        assert response == (None, None)