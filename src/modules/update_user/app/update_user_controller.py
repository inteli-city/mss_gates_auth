from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dtos.user_api_gateway_dto import UserApiGatewayDTO
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidCredentials, InvalidTokenError, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, Forbidden, InternalServerError, Unauthorized


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase
        self.mutable_fields = ['name', 'role']
    
    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if request.data.get('email') is None:
                raise MissingParameters('email')

            if request.data.get('systems') is None:
                raise MissingParameters('systems')
            
            if request.data.get('enabled') is None:
                raise MissingParameters('enabled')
            
            if request.data.get('role') is not None and request.data.get('role') not in [role.value for role in ROLE]:
                raise EntityError('role')
            
            user_data = {k: v for k, v in request.data.items() if k in self.mutable_fields}

            user = self.UpdateUserUsecase(
                new_user_data=user_data,
                user_email=request.data.get('email').lower(),
                systems=request.data.get('systems'),
                enabled=request.data.get('enabled'),
                requester_role=requester_user.role
            )

            viewmodel = UpdateUserViewmodel(user)
            return OK(viewmodel.to_dict())
        
        except MissingParameters as err:
            return BadRequest(body=f"Parâmetro ausente: {err.message}")

        except InvalidCredentials as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")

        except EntityError as err:
            return BadRequest(body=f"Parâmetro inválido: {err.message}")
        
        except NoItemsFound as err:
            return BadRequest(body=err.message)
        
        except InvalidTokenError as err:
            return Unauthorized(body="Token inválido ou expirado")
        
        except ForbiddenAction as err:
            return Forbidden(body=err.args[0])
        
        except Exception as err:
            return InternalServerError(body=err.args[0])