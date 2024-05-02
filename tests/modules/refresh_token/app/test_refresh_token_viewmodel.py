from src.modules.refresh_token.app.refresh_token_viewmodel import RefreshTokenViewmodel


class Test_RefreshTokenViewmodel:

    def test_refresh_token_viewmodel(self):
        access_token = 'valid_access_token-teste@gmail.com'
        refresh_token = "valid_refresh_token-teste@gmail.com"
        id_token = 'valid_refresh_token-teste@gmail.com'

        tokens = RefreshTokenViewmodel(access_token, refresh_token, id_token)

        expected = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'id_token': id_token,
            'message': "Token atualizado com sucesso!"
        }

        assert tokens.to_dict() == expected