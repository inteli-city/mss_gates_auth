from src.modules.get_all_users.app.get_all_users_viewmodel import GetAllUsersViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class Test_GetAllUsersViewmodel:

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                systems=[],
                enabled=True,
                user_status=USER_STATUS.CONFIRMED,
                ttl=123
                ))
        
        expected = {
            'user_id': '123',
            'name': 'Gabriel Godoy',
            'role': 'COLLABORATOR',
            'email': 'teste@gmail.com',
            'systems': [],
            'enabled': True,
            'user_status': 'CONFIRMED',
            'ttl': 123
        }

        assert viewmodel.to_dict() == expected
    
    def test_get_all_users_viewmodel(self):
        viewmodel = GetAllUsersViewmodel(
            users=[
                User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                systems=[],
                enabled=True,
                user_status=USER_STATUS.CONFIRMED, ttl=123)
            ])
        
        expected = {
            'users': [{
                'user_id': '123',
                'name': 'Gabriel Godoy',
                'role': 'COLLABORATOR',
                'email': 'teste@gmail.com',
                'systems': [],
                'enabled': True,
                'user_status': 'CONFIRMED',
                'ttl': 123
                }],
            'message': 'Usuários foram listados com sucesso!'
        }
    
        assert viewmodel.to_dict() == expected
