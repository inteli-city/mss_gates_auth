from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'email': 'teste123@gmail.com',
            'role': 'COLLABORATOR',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body['user']['user_id'] == '4'
        assert response.body['user']['name'] == 'Gabriel Godoy'
        assert response.body['user']['role'] == 'COLLABORATOR'
        assert response.body['user']['email'] == 'teste123@gmail.com'
        assert response.body['user']['systems'] == ['GAIA']
        assert response.body['user']['enabled'] == True
        assert response.body['user']['user_status'] == 'CONFIRMED'
        assert response.body['user']['ttl'] == 123
    
    def test_create_user_controller_no_requester_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste123@gmail.com',
            'role': 'COLLABORATOR',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: requester_user"
    
    def test_create_user_controller_no_role(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: role"
    
    def test_create_user_controller_role_not_valid(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'role': '123',
            'email': 'teste@gmail.com',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: role"

    
    def test_create_user_controller_no_name(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'email': 'teste@gmail.com',
            'role': 'COLLABORATOR',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: name"
    
    def test_create_user_controller_no_email(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'role': 'COLLABORATOR',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
    
    def test_create_user_controller_no_groups(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'COLLABORATOR',
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: systems"
    
    def test_create_user_controller_systems_not_valid(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@teste.com',
            'role': 'COLLABORATOR',
            'systems': ['123']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: systems"
    
    def test_create_user_controller_duplicated(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([system for system in repo.users[0].systems]),
                "custom:ttl": repo.users[0].ttl,
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'COLLABORATOR',
            'systems': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 409
        assert response.body == "Usuário ja cadastrado com esses dados"
