from src.modules.get_all_users.app.get_all_users_controller import GetAllUsersController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUsersUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersController:

    def test_get_all_users_controller(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)
        controller = GetAllUsersController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            }
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
                },
                {
                    'user_id': '2',
                    'name': 'Gabriel Godoy',
                    'role': 'COLLABORATOR',
                    'email': 'teste2@gmail.com',
                    'groups': [],
                    'enabled': True,
                    'user_status': 'UNCONFIRMED'
                },
                {
                    'user_id': '3',
                    'name': 'Gabriel Godoy',
                    'role': 'USER',
                    'email': 'teste3@gmail.com',
                    'groups': [],
                    'enabled': True,
                    'user_status': 'FORCE_CHANGE_PASSWORD'
                },
            ],
            'message': 'Usuários foram listados com sucesso!'
        }
    
    def test_get_all_users_controller_no_requester_user(self):
        repo = UserRepositoryMock()
        usecase = GetAllUsersUsecase(repo)
        controller = GetAllUsersController(usecase)

        request = HttpRequest(body={})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: requester_user"