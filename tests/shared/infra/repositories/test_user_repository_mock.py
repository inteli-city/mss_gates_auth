from typing import Tuple
from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
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
        assert users[0].groups == [GROUPS.GAIA]

    def test_get_user_by_email(self):
        repo = UserRepositoryMock()
        user = repo.get_user_by_email('teste@gmail.com')

        assert user.name == 'Gabriel Godoy'
        assert type(user) == User

    def test_create_user(self):
        repo = UserRepositoryMock()
        user = repo.create_user(email='teste3@gmail.com', name='Gabriel Godoy', role=ROLE.COLLABORATOR, groups=[])

        assert len(repo.users) == 4
        assert type(user) == User
        assert repo.users[-1].user_id == '4'
        assert repo.users[-1].email == 'teste3@gmail.com'
        assert repo.users[-1].name == 'Gabriel Godoy'
        assert repo.users[-1].role == ROLE.COLLABORATOR
        assert repo.users[-1].groups == []

    def test_get_users_in_group(self):
        repo = UserRepositoryMock()
        users = repo.get_users_in_group(GROUPS.GAIA)

        assert len(users) == 1
        assert type(users[0]) == User
        assert users[0].email == 'teste@gmail.com'
        assert users[0].name == 'Gabriel Godoy'
        assert users[0].role == ROLE.ADMIN_COLLABORATOR
        assert users[0].groups == [GROUPS.GAIA]
    
    def test_update_user(self):
        repo = UserRepositoryMock()
        user = repo.update_user(user_email='teste@gmail.com', kvp_to_update={'role': ROLE.USER}, addGroups=[GROUPS.JUNDIAI], removeGroups=[GROUPS.GAIA], enabled=False)

        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.role == ROLE.USER
        assert user.groups == [GROUPS.JUNDIAI]
        assert user.enabled == False
    
    def test_update_user_enabled_null(self):
        repo = UserRepositoryMock()
        user = repo.update_user(user_email='teste@gmail.com', kvp_to_update={'role': ROLE.USER}, addGroups=[GROUPS.JUNDIAI], removeGroups=[GROUPS.GAIA])

        assert user.email == 'teste@gmail.com'
        assert type(user) == User
        assert user.role == ROLE.USER
        assert user.groups == [GROUPS.JUNDIAI]
        assert user.enabled == True
    
    def test_refresh_token(self):
        repo = UserRepositoryMock()
        resp = repo.refresh_token(
            refresh_token="valid_refresh_token-teste@gmail.com")
        assert resp[0] == 'valid_access_token-teste@gmail.com'
        assert resp[1] == 'valid_refresh_token-teste@gmail.com'
        assert resp[2] == 'valid_id_token-teste@gmail.com'