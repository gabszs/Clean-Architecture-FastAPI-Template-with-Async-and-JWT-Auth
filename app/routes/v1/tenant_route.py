from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindBase
from app.core.dependencies import TenantServiceDependency
from app.schemas.tenant_schema import BaseTenant
from app.schemas.tenant_schema import Tenant
from app.schemas.tenant_schema import TenantList
from app.schemas.tenant_schema import UpdateTenant

router = APIRouter(prefix="/tenant", tags=["tenant"])


@router.get("/", response_model=TenantList)
async def get_tenant_list(
    service: TenantServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant_by_id(tenant_id: UUID, service: TenantServiceDependency, current_user: CurrentUserDependency):
    return await service.get_by_id(tenant_id)


@router.post("/", status_code=201, response_model=Tenant)
async def create_tenant(user: BaseTenant, service: TenantServiceDependency):
    return await service.add(user)


### importante tem de fazer
### adicionar validacao para quano o a request tiver parametros iguais ao do current_user
@router.put("/{tenant_id}", response_model=Tenant)
async def update_tenant(
    tenant_id: UUID, tenant: UpdateTenant, service: TenantServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=tenant_id, schema=tenant)


@router.delete("/{tenant_id}", status_code=204)
async def delete_user(tenant_id: UUID, service: TenantServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(tenant_id)
