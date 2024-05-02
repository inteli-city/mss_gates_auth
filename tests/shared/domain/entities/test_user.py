from src.shared.domain.entities.user import User
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.helpers.errors.domain_errors import EntityError
import pytest


class Test_User:
    def test_user(self):
        User(user_id="1", name="GODOY", email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)
    
    def test_user_user_id_is_not_str(self):
        with pytest.raises(EntityError):
            User(user_id=123, name="GODOY", email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)

    def test_user_name_is_none(self):
        with pytest.raises(EntityError):
            User(user_id="1",name=None, email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)

    def test_user_name_is_not_str(self):
        with pytest.raises(EntityError):
            User(user_id="1",name=123, email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)

    def test_user_name_is_shorter_than_min_length(self):
        with pytest.raises(EntityError):
            User(user_id="1",name="G", email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)

    def test_user_email_is_none(self):
        with pytest.raises(EntityError):
            User(user_id="1",name="GODOY", email=None, role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)

    def test_user_email_is_not_valid(self):
        with pytest.raises(EntityError):
            User(user_id="1",name="GODOY", email="teste", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)
    
    def test_user_email_is_not_str(self):
        with pytest.raises(EntityError):
            User(user_id="1",name='123', email=123, role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)
    
    def test_user_role_is_none(self):
        with pytest.raises(EntityError):
            User(user_id="1",name='GODOY', email="teste123@maua.br", role=None, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)

    def test_user_role_is_not_enum(self):
        with pytest.raises(EntityError):
            User(user_id="1",name='GODOY', email="teste123@maua.br", role=123, groups=[GROUPS.GAIA], enabled=True, user_status=USER_STATUS.CONFIRMED)
    
    def test_user_groups_is_not_list(self):
        with pytest.raises(EntityError):
            User(user_id="1",name='GODOY', email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=123, enabled=True, user_status=USER_STATUS.CONFIRMED)
    
    def test_user_enabled_is_not_bool(self):
        with pytest.raises(EntityError):
            User(user_id="1",name='GODOY', email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=123, user_status=USER_STATUS.CONFIRMED)
    
    def test_user_user_status_is_not_enum(self):
        with pytest.raises(EntityError):
            User(user_id="1",name='GODOY', email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=True, user_status=123)
    
    def test_user_parse_object(self):
        user = User.parse_object({
            "user_id": "1",
            'name': 'GODOY',
            'email': 'teste123@maua.br',
            'role': 'COLLABORATOR',
            'groups': ['GAIA'],
            'enabled': True,
            'user_status': 'CONFIRMED'
        })

        assert user.user_id == '1'
        assert user.name == 'Godoy'
        assert user.email == 'teste123@maua.br'
        assert user.role == ROLE.COLLABORATOR
        assert user.groups == [GROUPS.GAIA]
        assert user.enabled == True
        assert user.user_status == USER_STATUS.CONFIRMED

    def test_user_to_dict(self):
        user = User(user_id="1",name="GODOY", email="teste123@maua.br", role=ROLE.COLLABORATOR, groups=[GROUPS.GAIA], enabled=False, user_status=USER_STATUS.CONFIRMED)
        assert user.to_dict() == {
            'user_id': "1",
            'name': 'GODOY',
            'email': 'teste123@maua.br',
            'role': 'COLLABORATOR',
            'groups': ['GAIA'],
            'enabled': False,
            'user_status': 'CONFIRMED'
        }