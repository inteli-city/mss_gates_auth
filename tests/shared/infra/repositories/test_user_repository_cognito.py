import pytest
from src.shared.infra.repositories.user_repository_cognito import UserRepositoryCognito


class Test_UserRepositoryCognito:
    @pytest.mark.skip("Can't test it locally")
    def test_list_groups(self):
        repo = UserRepositoryCognito()
        repo.get_users_in_group("GAIA")

    @pytest.mark.skip("Can't test it locally")
    def test_get_user_by_email(self):
        repo = UserRepositoryCognito()
        repo.get_user_by_email("teste1234@gmail.com")
    
    @pytest.mark.skip("Can't test it locally")
    def test_get_all_users(self):
        repo = UserRepositoryCognito()
        repo.get_all_users()

        assert 1 == 0
    
    @pytest.mark.skip("Can't test it locally")
    def test_update_user_enabled(self):
        repo = UserRepositoryCognito()
        user = repo.update_user(user_email="gabriel.fortes@intelicitybr.com.br", 
                         kvp_to_update={"name": "Gabriel Fortes"},
                         enabled=True
                         )
        assert user.name == "Gabriel Fortes"
        assert user.enabled == True
    
    @pytest.mark.skip("Can't test it locally")
    def test_disable_user(self):
        repo = UserRepositoryCognito()
        repo.enable_user("gabriel.fortes@intelicitybr.com.br")