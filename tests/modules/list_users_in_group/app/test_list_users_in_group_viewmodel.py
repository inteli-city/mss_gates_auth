from src.modules.list_users_in_group.app.list_users_in_group_viewmodel import ListUsersInGroupViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class Test_ListUsersInGroupViewmodel:

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],
                enabled=True,
                user_status=USER_STATUS.CONFIRMED,
                ttl=123
                ))
        
        expected = {
            'user_id': '123',
            'name': 'Gabriel Godoy',
            'role': 'COLLABORATOR',
            'email': 'teste@gmail.com',
            'groups': [],
            'enabled': True,
            'user_status': 'CONFIRMED',
            'ttl': 123
        }

        assert viewmodel.to_dict() == expected
        
    def test_list_users_in_group_viewmodel(self):
        viewmodel = ListUsersInGroupViewmodel(
            users=[
                User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],
                enabled=True,
                user_status=USER_STATUS.CONFIRMED,
                ttl=123
                )
            ])
        
        expected = {
            'users': [{
                'user_id': '123',
                'name': 'Gabriel Godoy',
                'role': 'COLLABORATOR',
                'email': 'teste@gmail.com',
                'groups': [],
                'enabled': True,
                'user_status': 'CONFIRMED',
                'ttl': 123
                }],
            'message': 'Usuários foram listados com sucesso!'
        }
    
        assert viewmodel.to_dict() == expected
    