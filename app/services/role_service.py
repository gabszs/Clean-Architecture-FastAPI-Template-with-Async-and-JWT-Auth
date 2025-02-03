from app.repository import RoleRepository
from app.services.base_service import BaseService


class RoleService(BaseService):
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository
        super().__init__(role_repository)
