import datetime
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.enums.user_status_enum import USER_STATUS
from src.shared.infra.dtos.user_cognito_dto import UserCognitoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserCognitoDTO:

    def test_from_entity(self):
        user = User(user_id="1", email="joao@hotmail.com", name='João', role=ROLE.COLLABORATOR, systems=["GAIA"], enabled=True, user_status=USER_STATUS.CONFIRMED, ttl=123)

        user_cognito_dto = UserCognitoDTO.from_entity(user)

        user_cognito_dto_expected = UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            role=user.role,
            systems=user.systems,
            enabled=user.enabled,
            user_status=user.user_status,
            ttl=user.ttl
        )

        assert user_cognito_dto.user_id == user_cognito_dto_expected.user_id
        assert user_cognito_dto.email == user_cognito_dto_expected.email
        assert user_cognito_dto.name == user_cognito_dto_expected.name
        assert user_cognito_dto.role == user_cognito_dto_expected.role
        assert user_cognito_dto.systems == user_cognito_dto_expected.systems
        assert user_cognito_dto.enabled == user_cognito_dto_expected.enabled
        assert user_cognito_dto.user_status == user_cognito_dto_expected.user_status
        assert user_cognito_dto.ttl == user_cognito_dto_expected.ttl

    def test_from_entity_none(self):
        user = User(user_id="1", email="joao@hotmail.com", name='João', role=ROLE.COLLABORATOR, systems=["GAIA"], enabled=True, user_status=USER_STATUS.CONFIRMED, ttl=123)
        user_cognito_dto = UserCognitoDTO.from_entity(user)

        user_cognito_dto_expected = UserCognitoDTO(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            role=user.role,
            systems=user.systems,
            enabled=user.enabled,
            user_status=user.user_status,
            ttl=user.ttl
        )
        
        assert user_cognito_dto.user_id == user_cognito_dto_expected.user_id
        assert user_cognito_dto.email == user_cognito_dto_expected.email
        assert user_cognito_dto.name == user_cognito_dto_expected.name
        assert user_cognito_dto.role == user_cognito_dto_expected.role
        assert user_cognito_dto.systems == user_cognito_dto_expected.systems
        assert user_cognito_dto.enabled == user_cognito_dto_expected.enabled
        assert user_cognito_dto.user_status == user_cognito_dto_expected.user_status
        assert user_cognito_dto.ttl == user_cognito_dto_expected.ttl

    def test_from_cognito(self):
        data = {
                        'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                                             'content-length': '709',
                                                             'content-type': 'application/x-amz-json-1.1',
                                                             'date': 'Sat, 04 Feb 2023 13:45:05 GMT',
                                                             'x-amzn-requestid': '8b8fba2d-b2c7-4346-a441-e285892af0a3'},
                                             'HTTPStatusCode': 200,
                                             'RequestId': '8b8fba2d-b2c7-4346-a441-e285892af0a3',
                                             'RetryAttempts': 0},
                        'UserAttributes': [{'Name': 'custom:general_role', 'Value': 'COLLABORATOR'},
                                           {'Name': 'name', 'Value': 'joao'},
                                           {'Name': 'email', 'Value': 'joao@hotmail.com'},
                                            {'Name': 'sub',
                                        'Value': '123'},
                                            {'Name': 'custom:ttl', 'Value': '123'},
                                           ],
                        'UserCreateDate': datetime.datetime(2023, 2, 3, 23, 27, 48, 713000),
                        'UserLastModifiedDate': datetime.datetime(2023, 2, 3, 23, 27, 48, 713000),
                        'UserStatus': 'UNCONFIRMED',
                        'Enabled': 'true',
                        'Username': 'gabriel@gmail.com'}

        user_cognito_dto = UserCognitoDTO.from_cognito(data)

        expected_dto = UserCognitoDTO(
            user_id="123",
            email="joao@hotmail.com",
            name="joao",
            role=ROLE.COLLABORATOR,
            enabled=True,
            user_status=USER_STATUS.UNCONFIRMED,
            ttl=123
        )

        assert user_cognito_dto.user_id == expected_dto.user_id
        assert user_cognito_dto.email == expected_dto.email
        assert user_cognito_dto.name == expected_dto.name
        assert user_cognito_dto.role == expected_dto.role
        assert user_cognito_dto.enabled == expected_dto.enabled
        assert user_cognito_dto.user_status == expected_dto.user_status
        assert user_cognito_dto.ttl == expected_dto.ttl
    
    def test_to_cognito_attributes(self):
        user_cognito_dto = UserCognitoDTO(
            user_id="123",
            email="joao@hotmail.com",
            name="joao",
            role=ROLE.COLLABORATOR,
            systems=["GAIA"],
            enabled=True,
            user_status=USER_STATUS.CONFIRMED,
            ttl=123
        )
        cognito = user_cognito_dto.to_cognito_attributes()

        assert cognito[0]['Name'] == 'email'
        assert cognito[0]['Value'] == 'joao@hotmail.com'
        assert cognito[1]['Name'] == 'name'
        assert cognito[1]['Value'] == 'joao'
        assert cognito[2]['Name'] == 'custom:general_role'
        assert cognito[2]['Value'] == 'COLLABORATOR'
        assert cognito[3]['Name'] == 'custom:ttl'
        assert cognito[3]['Value'] == '123'
        assert len(cognito) == 4


    def test_to_entity(self):
        repo = UserRepositoryMock()

        user_cognito_dto = UserCognitoDTO(
            user_id = repo.users[0].user_id,
            email = repo.users[0].email,
            name = repo.users[0].name,
            role = repo.users[0].role,
            systems = repo.users[0].systems,
            enabled = repo.users[0].enabled,
            user_status = repo.users[0].user_status,
            ttl = repo.users[0].ttl
        )

        user = user_cognito_dto.to_entity()

        assert user.user_id == repo.users[0].user_id
        assert user.email == repo.users[0].email
        assert user.name == repo.users[0].name
        assert user.role == repo.users[0].role
        assert user.systems == repo.users[0].systems
        assert user.enabled == repo.users[0].enabled
        assert user.user_status == repo.users[0].user_status
        assert user.ttl == repo.users[0].ttl