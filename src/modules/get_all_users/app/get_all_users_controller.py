from src.shared.infra.dtos.user_api_gateway_dto import UserApiGatewayDTO
from .get_all_users_usecase import GetAllUsersUsecase
from .get_all_users_viewmodel import GetAllUsersViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidCredentials, InvalidTokenError, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, Unauthorized


class GetAllUsersController:
    def __init__(self, usecase: GetAllUsersUsecase) -> None:
        self.getAllUsersUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            list_users = self.getAllUsersUsecase(requester_role=requester_user.role)

            viewmodel = GetAllUsersViewmodel(users=list_users)

            return OK(viewmodel.to_dict())
        
        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")
        
        except ForbiddenAction as err:
            return Forbidden(body=err.args[0])

        except Exception as err:
            return InternalServerError(body=err.args[0])