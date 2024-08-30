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
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            }
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'users': [
                {
                    'user_id': '1',
                    'name': 'Gabriel Godoy',
                    'role': 'ADMIN_COLLABORATOR',
                    'email': 'teste@gmail.com',
                    'systems': ['GAIA'],
                    'enabled': True,
                    'user_status': 'CONFIRMED',
                    'ttl': 123
                },
                {
                    'user_id': '2',
                    'name': 'Gabriel Godoy',
                    'role': 'COLLABORATOR',
                    'email': 'teste2@gmail.com',
                    'systems': [],
                    'enabled': True,
                    'user_status': 'UNCONFIRMED',
                    'ttl': 123
                },
                {
                    'user_id': '3',
                    'name': 'Gabriel Godoy',
                    'role': 'USER',
                    'email': 'teste3@gmail.com',
                    'systems': [],
                    'enabled': True,
                    'user_status': 'FORCE_CHANGE_PASSWORD',
                    'ttl': 123
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