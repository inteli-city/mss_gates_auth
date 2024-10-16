from src.modules.create_user.app.create_user_viewmodel import CreateUserViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class Test_CreateUserViewmodel:

    def test_create_user_viewmodel(self):
        viewmodel = CreateUserViewmodel(
            user=User(user_id="123",role=ROLE.COLLABORATOR,
            name='Gabriel Godoy',
            email='teste@gmail.com',
            systems=[],
            enabled=True,
            user_status=USER_STATUS.FORCE_CHANGE_PASSWORD,
            ttl=123
            )
        )

        expected = {
            'user': {
                'user_id': '123',
                'name': 'Gabriel Godoy',
                'role': 'COLLABORATOR',
                'email': 'teste@gmail.com',
                'systems': [],
                'enabled': True,
                'user_status': 'FORCE_CHANGE_PASSWORD',
                'ttl': 123
            },
            'message': 'Usuário foi criado com sucesso!'
        }

        assert viewmodel.to_dict() == expected

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                systems=[],
            enabled=True,
            user_status=USER_STATUS.FORCE_CHANGE_PASSWORD, ttl=123))
        
        expected = {
            'user_id': '123',
            'name': 'Gabriel Godoy',
            'role': 'COLLABORATOR',
            'email': 'teste@gmail.com',
            'systems': [],
            'enabled': True,
            'user_status': 'FORCE_CHANGE_PASSWORD',
            'ttl': 123
        }

        assert viewmodel.to_dict() == expected