from .get_user_usecase import GetUserUsecase
from .get_user_viewmodel import GetUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, InvalidCredentials
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Conflict, Forbidden, InternalServerError


class GetUserController:
    def __init__(self, usecase: GetUserUsecase) -> None:
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('access_token') is None:
                raise MissingParameters('access_token')
            
            user = self.usecase(access_token=request.data.get('access_token'))

            viewmodel = GetUserViewmodel(user)
            response = OK(viewmodel.to_dict())
            
            return response
        
        except DuplicatedItem as err:
            return Conflict(body=f"Usuário ja cadastrado com esses dados")

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")
        
        except ForbiddenAction as err:
            return Forbidden(body=err.args[0])
        
        except Exception as err:
            return InternalServerError(body=err.args[0])