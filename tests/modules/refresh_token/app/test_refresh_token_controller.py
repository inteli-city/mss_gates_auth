from src.modules.refresh_token.app.refresh_token_controller import RefreshTokenController
from src.modules.refresh_token.app.refresh_token_usecase import RefreshTokenUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_RefreshTokenController:
    def test_refresh_token_controller(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo)
        controller = RefreshTokenController(usecase)

        header = {"refresh_token": "valid_refresh_token-teste@gmail.com"}
        request = HttpRequest(headers=header)

        response = controller(request)

        assert response.status_code == 200
        assert response.body['access_token'] == "valid_access_token-teste@gmail.com"
        assert response.body['refresh_token'] == "valid_refresh_token-teste@gmail.com"
        assert response.body['id_token'] == "valid_id_token-teste@gmail.com"
        assert response.body['message'] == "Token atualizado com sucesso!"

    def test_refresh_token_controller_missing_authorization(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo)
        controller = RefreshTokenController(usecase)

        request = HttpRequest()

        response = controller(request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro ausente: refresh_token'


    def test_refresh_token_controller_invalid_refresh_token(self):
        repo = UserRepositoryMock()
        usecase = RefreshTokenUsecase(repo)
        controller = RefreshTokenController(usecase)

        headers = {"refresh_token": "invalid_refresh_token-teste@gmail.com"}

        request = HttpRequest(headers=headers)
        reponse = controller(request)

        assert reponse.status_code == 403
        assert reponse.body == 'Sem autorização para: Refresh Token'