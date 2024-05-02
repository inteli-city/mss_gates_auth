from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UpdateUserController:

    def test_update_user_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'USER',
            'groups': ['GAIA'],
            'enabled': True
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body == {
            'user': {
                'user_id': '1',
                'name': 'Gabriel Godoy',
                'role': 'USER',
                'email': 'teste@gmail.com',
                'groups': ['GAIA'],
                'enabled': True,
                'user_status': 'CONFIRMED'
            }, 
            'message': 'Usuário foi atualizado com sucesso!'
        }
    
    def test_update_user_controller_no_requester_user(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={
            'name': 'Gabriel Godoy',
            'email': 'teste@gmail.com',
            'role': 'USER',
            'groups': ['GAIA'],
            'enabled': True
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: requester_user"
    
    def test_update_user_controller_no_email(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'groups': ['GAIA'],
            'enabled': True
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: email"
    
    def test_update_user_controller_no_groups(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'email': 'teste@gmail.com',
            'enabled': True
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: groups"
    
    def test_update_user_controller_groups_not_set(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'email': 'teste@gmail.com',
            'groups': ['123'],
            'enabled': True
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro inválido: groups"
    
    def test_update_user_controller_no_enabled(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo)
        controller = UpdateUserController(usecase)

        request = HttpRequest(body={"requester_user": {
                "sub": repo.users[0].user_id,
                "name": repo.users[0].name,
                "email": repo.users[0].email,
                "custom:general_role": repo.users[0].role.value,
                "cognito:groups": ','.join([group.value for group in repo.users[0].groups])
            },
            'name': 'Gabriel Godoy',
            'role': 'USER',
            'email': 'teste@gmail.com',
            'groups': ['GAIA']
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Parâmetro ausente: enabled"