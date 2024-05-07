import pytest
from src.modules.list_users_in_group.app.list_users_in_group_usecase import ListUsersInGroupUsecase
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersInGroupUsecase:

    def test_list_users_in_group_usecase(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)
        users_response = usecase(group=GROUPS.GAIA, request_user_role=ROLE.ADMIN_COLLABORATOR, request_user_groups=[GROUPS.GAIA])

        assert len(users_response) == 1
    
    def test_list_users_in_group_usecase_user_not_allowed(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(group=GROUPS.GAIA, request_user_role=ROLE.USER, request_user_groups=[GROUPS.GAIA])
    
    def test_list_users_in_group_usecase_user_not_in_group(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(group=GROUPS.JUNDIAI, request_user_role=ROLE.ADMIN_COLLABORATOR, request_user_groups=[GROUPS.GAIA])
    

    def test_list_users_in_group_usecase_with_user_not_in_group(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)

        with pytest.raises(ForbiddenAction):
            usecase(group=GROUPS.GAIA, request_user_role=ROLE.USER, request_user_groups=[GROUPS.JUNDIAI])