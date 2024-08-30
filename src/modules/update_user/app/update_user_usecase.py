from typing import List
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class UpdateUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo
        self.immutable_fields = ['email', 'systems']
        self.mutable_fields = ['name', 'role']

    def __call__(self, new_user_data: dict, user_email: str, systems: List[str], enabled: bool, requester_role: ROLE) -> User:

        if requester_role != ROLE.ADMIN_COLLABORATOR:
            raise ForbiddenAction("Usuário não tem permissão para alterar usuários")

        old_user = self.repo.get_user_by_email(user_email)

        if old_user is None:
            raise NoItemsFound("user")
        
        if old_user.enabled == enabled:
            enabled = None

        old_user_data = User.to_dict(old_user)

        kvp_to_update = {k: v for k, v in new_user_data.items() if k in self.mutable_fields and v is not None}

        bool_items = [User.__annotations__[k] for k in self.mutable_fields if User.__annotations__[k] == bool]

        kvp_to_update = {k: eval(v.title()) if User.__annotations__[k] in bool_items and type(v) == str else v for k, v in kvp_to_update.items()}

        for k, v in kvp_to_update.items():
            old_user_data[k] = v if v != "" else None

        kvp_to_update = {k: str(v) for k, v in kvp_to_update.items()}

        add_systems = [system for system in systems if system not in old_user.systems]
        remove_systems = [system for system in old_user.systems if system not in systems]

        add_systems = add_systems if add_systems else None
        remove_systems = remove_systems if remove_systems else None

        user_response = self.repo.update_user(user_email=user_email, kvp_to_update=kvp_to_update, addSystems=add_systems, removeSystems=remove_systems, enabled=enabled)

        return user_response