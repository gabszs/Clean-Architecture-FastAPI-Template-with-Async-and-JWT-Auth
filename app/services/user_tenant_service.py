from app.repository import UserTenantRepository
from app.services.base_service import BaseService


class UserTenantService(BaseService):
    def __init__(self, user_tenant_repository: UserTenantRepository):
        self.user_tenant_repository = user_tenant_repository
        super().__init__(user_tenant_repository)
