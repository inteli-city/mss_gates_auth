import json
from src.modules.refresh_token.app.refresh_token_presenter import lambda_handler


class Test_RefreshTokenPresenter:

    def test_refresh_token_presenter(self):
        event = {
            "body": {
                'refresh_token': 'valid_refresh_token-teste@gmail.com'
            }
        }

        response = lambda_handler(event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == 'Token atualizado com sucesso!'