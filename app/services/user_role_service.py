from app.repository import UserRoleRepository
from app.services.base_service import BaseService


class UserRoleService(BaseService):
    def __init__(self, user_role_repository: UserRoleRepository):
        self.user_role_repository = user_role_repository
        super().__init__(user_role_repository)
