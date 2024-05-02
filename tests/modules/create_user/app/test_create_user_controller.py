from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_CreateUserController:

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)
        header = {"Authorization": "Bearer valid_access_token-teste@gmail.com"}

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'email': 'teste123@gmail.com',
            'role': 'COLLABORATOR',
            'groups': ['GAIA']
        }, headers=header)

        response = controller(request)

        assert response.status_code == 201
        assert response.body == {
            'user': {
                'user_id': '4',
                'name': 'Gabriel Godoy',
                'role': 'COLLABORATOR',
                'email': 'teste123@gmail.com',
                'groups': ['GAIA'],
                'enabled': True,
                'user_status': 'CONFIRMED'
            }, 
            'message': 'Usuário foi criado com sucesso!'
        }
    
    def test_create_user_controller_no_requester_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)
        controller = CreateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste123@gmail.com',
            'role': 'COLLABORATOR',
            'groups': ['GAIA']
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
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
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
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'role': '123',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
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
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'email': 'teste@gmail.com',
            'role': 'COLLABORATOR',
            'groups': ['GAIA']
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
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'role': 'COLLABORATOR',
            'groups': ['GAIA']
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
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'COLLABORATOR',
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: groups"
