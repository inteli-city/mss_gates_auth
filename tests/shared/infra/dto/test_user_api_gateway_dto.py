from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dtos.user_api_gateway_dto import UserApiGatewayDTO

class Test_UserApiGatewayDTO:
    
    def test_user_api_gateway_dto_from_api_gateway(self):
        user_data = {
            'sub': 'd61dbf66-a10f-11ed-a8fc-0242ac120002',
            'name': 'Gabriel Godoy',
            'email': 'gabriel.godoy@gmail.com', 
            'custom:general_role': 'ADMIN_COLLABORATOR',
            'cognito:groups': "GAIA,JUNDIAI",
            'custom:ttl': '123'
            }

        user_dto = UserApiGatewayDTO.from_api_gateway(user_data)

        expected_user_dto = UserApiGatewayDTO(
            user_id = "d61dbf66-a10f-11ed-a8fc-0242ac120002",
            name = "Gabriel Godoy",
            email = "gabriel.godoy@gmail.com",
            role = ROLE.ADMIN_COLLABORATOR,
            systems = ["GAIA", "JUNDIAI"],
            ttl = 123
            )
                
        assert user_dto == expected_user_dto