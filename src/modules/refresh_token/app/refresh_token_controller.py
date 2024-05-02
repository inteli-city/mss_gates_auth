from .refresh_token_usecase import RefreshTokenUsecase
from .refresh_token_viewmodel import RefreshTokenViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidTokenError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, Unauthorized


class RefreshTokenController:

    def __init__(self, usecase: RefreshTokenUsecase):
        self.refreshTokenUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:            
            if request.data.get('refresh_token') is None:
                raise MissingParameters('refresh_token')

            refresh_token = request.data.get('refresh_token')

            tokens = self.refreshTokenUsecase(refresh_token)
            
            access_token, refresh_token, id_token = tokens

            refresh_token_viewmodel = RefreshTokenViewmodel(
                access_token=access_token, refresh_token=refresh_token, id_token=id_token)
            
            response = OK(refresh_token_viewmodel.to_dict())

            
            return response

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except ForbiddenAction as err:
            return Forbidden(body=f"Sem autorização para: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except InvalidTokenError as err:
            return Unauthorized(body="Token inválido ou expirado")
        
        except Exception as err:
            return InternalServerError(body=err.args[0])