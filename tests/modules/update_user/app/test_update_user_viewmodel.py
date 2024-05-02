from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel, UserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS


class Test_UpdateUserViewmodel:

    def test_user_viewmodel(self):
        viewmodel = UserViewmodel(User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],
                enabled=True,
                user_status=USER_STATUS.CONFIRMED))
        
        expected = {
            'user_id': '123',
            'name': 'Gabriel Godoy',
            'role': 'COLLABORATOR',
            'email': 'teste@gmail.com',
            'groups': [],
            'enabled': True,
            'user_status': 'CONFIRMED'
        }

        assert viewmodel.to_dict() == expected
    
    def test_update_user_viewmodel(self):
        viewmodel = UpdateUserViewmodel(
            
                User(user_id="123",role=ROLE.COLLABORATOR,
                name='Gabriel Godoy',
                email='teste@gmail.com',
                groups=[],
                enabled=True,
                user_status=USER_STATUS.CONFIRMED)
            )
        
        expected = {
            'user': {
                'user_id': '123',
                'name': 'Gabriel Godoy',
                'role': 'COLLABORATOR',
                'email': 'teste@gmail.com',
                'groups': [],
                'enabled': True,
                'user_status': 'CONFIRMED'
                },
            'message': 'Usuário foi atualizado com sucesso!'
        }
    
        assert viewmodel.to_dict() == expected