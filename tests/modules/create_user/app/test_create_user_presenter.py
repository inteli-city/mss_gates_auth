import json
from src.modules.create_user.app.create_user_presenter import lambda_handler


class Test_CreateUserPresenter:
    
        def test_create_user_presenter(self):
            event = {
                "version": "2.0",
                "routeKey": "$default",
                "rawPath": "/my/path",
                "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
                "cookies": [
                    "cookie1",
                    "cookie2"
                ],
                "headers": {
                    "header1": "value1",
                    "header2": "value1,value2"
                },
                "queryStringParameters": {
                    "parameter1": "1"
                },
                "requestContext": {
                    "accountId": "123456789012",
                    "apiId": "<urlid>",
                    "authentication": None,
                    "authorizer": {
                        "claims":
                            {
                                "sub": "1",
                                "name": "Gabriel Godoy",
                                "email": "gabriel@gmail.com",
                                "custom:general_role": "ADMIN_COLLABORATOR",
                                "cognito:groups": "GAIA"
                            }
                    },
                    "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                    "domainPrefix": "<url-id>",
                    "external_interfaces": {
                        "method": "POST",
                        "path": "/my/path",
                        "protocol": "HTTP/1.1",
                        "sourceIp": "123.123.123.123",
                        "userAgent": "agent"
                    },
                    "requestId": "id",
                    "routeKey": "$default",
                    "stage": "$default",
                    "time": "12/Mar/2020:19:03:58 +0000",
                    "timeEpoch": 1583348638390
                },
                "pathParameters": None,
                "isBase64Encoded": None,
                "stageVariables": None,
                "body": {
                    'name': 'Gabriel Godoy',
                    'email': 'teste@gmail.com',
                    'role': 'USER',
                    'groups': ['GAIA'],
                }
            }

            response = lambda_handler(event, None)
            assert response["statusCode"] == 201
            assert json.loads(response["body"])["message"] == 'Usuário foi criado com sucesso!'