from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindBase
from app.core.dependencies import UserTenantServiceDependency

from app.schemas.user_tenant_schema import BaseUserTenant
from app.schemas.user_tenant_schema import UserTenant
from app.schemas.user_tenant_schema import UserTenantList
from app.schemas.user_tenant_schema import UpdateUserTenant

router = APIRouter(prefix="/user-tenant", tags=["user-tenant"])


@router.get("/", response_model=UserTenantList)
async def get_user_tenant_list(
    service: UserTenantServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{user_tenant_id}", response_model=UserTenant)
async def get_user_tenant_by_id(user_tenant_id: UUID, service: UserTenantServiceDependency, current_user: CurrentUserDependency):
    return await service.get_by_id(user_tenant_id)


@router.post("/", status_code=201, response_model=UserTenant)
async def create_user_tenant(user_tenant: BaseUserTenant, service: UserTenantServiceDependency):
    return await service.add(user_tenant)


### importante tem de fazer
### adicionar validacao para quano o a request tiver parametros iguais ao do current_user
@router.put("/{user_tenant_id}", response_model=UserTenant)
async def update_user_tenant(
    user_tenant_id: UUID, user_tenant: UpdateUserTenant, service: UserTenantServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=user_tenant_id, schema=UserTenant)


@router.delete("/{user_tenant_id}", status_code=204)
async def delete_user_tenant(user_tenant_id: UUID, service: UserTenantServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(user_tenant_id)
