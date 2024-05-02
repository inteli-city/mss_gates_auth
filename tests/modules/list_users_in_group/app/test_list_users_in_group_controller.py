from src.modules.list_users_in_group.app.list_users_in_group_controller import ListUsersInGroupController
from src.modules.list_users_in_group.app.list_users_in_group_usecase import ListUsersInGroupUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_ListUsersInGroupController:

    def test_list_users_in_group_controller(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)
        controller = ListUsersInGroupController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'group': 'GAIA'
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'users': [
                {
                    'user_id': '1',
                    'name': 'Gabriel Godoy',
                    'role': 'COLLABORATOR',
                    'email': 'teste@gmail.com',
                    'groups': ['GAIA'],
                    'enabled': True,
                    'user_status': 'CONFIRMED'
                }
            ],
            'message': 'Usuários foram listados com sucesso!'
        }
    
    def test_list_users_in_group_controller_no_requester_user(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)
        controller = ListUsersInGroupController(usecase)

        request = HttpRequest(body={
            'group': 'GAIA'
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: requester_user"
    
    def test_list_users_in_group_controller_no_group(self):
        repo = UserRepositoryMock()
        usecase = ListUsersInGroupUsecase(repo)
        controller = ListUsersInGroupController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            }
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: group"