import datetime
import json
import time
from typing import Tuple, List

import boto3
from botocore.exceptions import ClientError

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, InvalidCredentials, InvalidTokenError
from src.shared.infra.dtos.user_cognito_dto import UserCognitoDTO


class UserRepositoryCognito(IUserRepository):

    client: boto3.client
    user_pool_id: str
    client_id: str

    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=Environments.get_envs().region)
        self.user_pool_id = Environments.get_envs().user_pool_id
        self.client_id = Environments.get_envs().client_id
    
    def get_user_by_access_token(self, access_token: str) -> User:
        try:
            response = self.client.get_user(
                AccessToken=access_token
            )

            if response.get('UserStatus') == 'UNCONFIRMED':
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
            user.systems = self.get_systems_for_user(user.email)
            return user

        except self.client.exceptions.NotAuthorizedException:
            raise InvalidCredentials("token")
    
    def get_all_users(self) -> List[User]:
        try:
            kwargs = {
                'UserPoolId': self.user_pool_id
            }

            all_users = list()
            users_remain = True
            next_page = None

            while users_remain:
                if next_page:
                    kwargs['PaginationToken'] = next_page
                response = self.client.list_users(**kwargs)


                all_users.extend(response["Users"])
                next_page = response.get('PaginationToken', None)
                users_remain = next_page is not None
        
            all_users = [UserCognitoDTO.from_cognito(user).to_entity() for user in all_users]

            for user in all_users:
                user.systems = self.get_systems_for_user(user.email)
            
            return all_users

        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def get_systems_for_user(self, email: str) -> List[str]:
        try:
            response = self.client.admin_list_groups_for_user(
                Username=email,
                UserPoolId=self.user_pool_id
            )
            systems = [system.get('GroupName') for system in response.get('Groups')]
            return systems
        except self.client.exceptions.UserNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

    
    def get_user_by_email(self, email: str) -> User:
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=email
            )
            if response["UserStatus"] == "UNCONFIRMED":
                return None

            user = UserCognitoDTO.from_cognito(response).to_entity()
            user.systems = self.get_systems_for_user(email)
                
            return user

        except self.client.exceptions.UserNotFoundException:
            return None
    
    def create_user(self, email: str, name: str, role: ROLE, systems: List[str]) -> User:

        # Obter a data e hora atual
        now = datetime.datetime.now()

        # Adicionar 90 dias
        future_date = now + datetime.timedelta(days=90)

        # Converter para timestamp em milissegundos
        ttl = str(int(future_date.timestamp() * 1000))

        cognito_attributes = [
            {
                "Name": "email",
                "Value": email
            },
            {
                "Name": "name",
                "Value": name
            },
            {
                "Name": "custom:general_role",
                "Value": role.value
            },
            {
                "Name": "custom:ttl",
                "Value": ttl
            }
        ]
        cognito_attributes.append({
            "Name": "email_verified",
            "Value": "True"
        })

        try:

            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                DesiredDeliveryMediums=["EMAIL"],
                UserAttributes=cognito_attributes)
            
            for system in systems:
                self.client.admin_add_user_to_group(
                    UserPoolId=self.user_pool_id,
                    Username=email,
                    GroupName=system
                )
                
            return self.get_user_by_email(email)

        except self.client.exceptions.UsernameExistsException:
            raise DuplicatedItem("user")

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def get_users_in_system(self, system: str) -> List[User]:
        try:
            users = []
            response = self.client.list_users_in_group(
                UserPoolId=self.user_pool_id,
                GroupName=system
            )

            for user in response.get('Users'):
                user = UserCognitoDTO.from_cognito(user).to_entity()
                user.systems = self.get_systems_for_user(user.email)
                users.append(user)
            
            return users

        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def update_user(self, user_email: str, kvp_to_update: dict, addSystems: List[str] = None, removeSystems: List[str] = None, enabled: bool = None) -> User:
        try:

            response = self.client.admin_update_user_attributes(
                UserPoolId=self.user_pool_id,
                Username=user_email,
                UserAttributes=[{'Name': UserCognitoDTO.TO_COGNITO_DICT[key], 'Value': value} for key, value in kvp_to_update.items()]
            )

            if addSystems is not None:
                for system in addSystems:
                    self.add_user_to_system(user_email, system)
            
            if removeSystems is not None:
                for system in removeSystems:
                    self.remove_user_from_system(user_email, system)


            user = self.get_user_by_email(user_email)

            if enabled is not None:
                if enabled:
                    self.enable_user(user_email)
                else:
                    self.disable_user(user_email)
                user.enabled = enabled
            
            self.sign_out_user(user_email)
            

            return user

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def enable_user(self, user_email: str) -> None:
        try:
            self.client.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=user_email
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def disable_user(self, user_email: str) -> None:
        try:
            self.client.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=user_email
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def add_user_to_system(self, user_email: str, system: str) -> None:
        try:
            self.client.admin_add_user_to_group(
                UserPoolId=self.user_pool_id,
                Username=user_email,
                GroupName=system
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def remove_user_from_system(self, user_email: str, system: str) -> None:
        try:
            self.client.admin_remove_user_from_group(
                UserPoolId=self.user_pool_id,
                Username=user_email,
                GroupName=system
            )
        except self.client.exceptions.ResourceNotFoundException as e:
            raise EntityError(e.response.get('Error').get('Message'))

        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))
    
    def refresh_token(self, refresh_token: str) -> Tuple[str, str, str]:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refresh_token
                }
            )

            id_token = response["AuthenticationResult"]["IdToken"]
            access_token = response["AuthenticationResult"]["AccessToken"]

            return access_token, refresh_token, id_token
        except ClientError as e:
            errorCode = e.response.get('Error').get('Code')
            if errorCode == 'NotAuthorizedException':
                raise InvalidTokenError(message="token")
            else:
                raise ForbiddenAction(message=e.response.get('Error').get('Message'))
    
    def sign_out_user(self, email: str) -> None:
        try:
            self.client.admin_user_global_sign_out(
                UserPoolId=self.user_pool_id,
                Username=email
            )
        except self.client.exceptions.InvalidParameterException as e:
            raise EntityError(e.response.get('Error').get('Message'))