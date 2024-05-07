from src.shared.infra.dtos.user_api_gateway_dto import UserApiGatewayDTO
from .list_users_in_group_usecase import ListUsersInGroupUsecase
from .list_users_in_group_viewmodel import ListUsersInGroupViewmodel
from src.shared.domain.enums.groups_enum import GROUPS
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import InvalidCredentials, InvalidTokenError, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, Unauthorized


class ListUsersInGroupController:
    def __init__(self, usecase: ListUsersInGroupUsecase) -> None:
        self.listUsersInGroupUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if request.data.get('group') is None:
                raise MissingParameters('group')

            if request.data.get('group') not in [g.value for g in GROUPS]:
                    raise EntityError('group')
            
            list_users = self.listUsersInGroupUsecase(group=GROUPS[request.data.get('group')], request_user_role=requester_user.role, request_user_groups=requester_user.groups)

            viewmodel = ListUsersInGroupViewmodel(users=list_users)

            return OK(viewmodel.to_dict())

        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")
        
        except Exception as err:
            return InternalServerError(body=err.args[0])