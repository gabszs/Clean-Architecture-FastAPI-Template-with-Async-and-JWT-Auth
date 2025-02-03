from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindBase
from app.core.dependencies import RoleServiceDependency
from app.core.security import authorize
from app.models.models_enums import UserRoles
from app.schemas.role_schema import BaseRole
from app.schemas.role_schema import Role
from app.schemas.role_schema import RoleList
from app.schemas.role_schema import UpdateRole

router = APIRouter(prefix="/role", tags=["role"])


@router.get("/", response_model=RoleList)
@authorize(role=[UserRoles.ADMIN])
async def get_role_list(
    service: RoleServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{role_id}", response_model=Role)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN], allow_same_id=True)
async def get_role_by_id(role_id: UUID, service: RoleServiceDependency, current_user: CurrentUserDependency):
    return await service.get_by_id(role_id)


@router.post("/", status_code=201, response_model=Role)
async def create_role(user: BaseRole, service: RoleServiceDependency):
    return await service.add(user)


### importante tem de fazer
### adicionar validacao para quano o a request tiver parametros iguais ao do current_user
@router.put("/{role_id}", response_model=Role)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN], allow_same_id=True)
async def update_role(
    role_id: UUID, role: UpdateRole, service: RoleServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=role_id, schema=role)


@router.delete("/{role_id}", status_code=204)
@authorize(role=[UserRoles.ADMIN])
async def delete_user(role_id: UUID, service: RoleServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(role_id)
