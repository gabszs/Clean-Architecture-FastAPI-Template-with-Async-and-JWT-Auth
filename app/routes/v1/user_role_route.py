from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindBase
from app.core.dependencies import UserRoleServiceDependency

from app.schemas.user_role_schema import BaseUserRole
from app.schemas.user_role_schema import UserRole
from app.schemas.user_role_schema import UserRoleList
from app.schemas.user_role_schema import UpdateUserRole

router = APIRouter(prefix="/user-role", tags=["user-role"])


@router.get("/", response_model=UserRoleList)
async def get_user_role_list(
    service: UserRoleServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{user_role_id}", response_model=UserRole)
async def get_user_role_by_id(user_role_id: UUID, service: UserRoleServiceDependency, current_user: CurrentUserDependency):
    return await service.get_by_id(user_role_id)


@router.post("/", status_code=201, response_model=UserRole)
async def create_user_role(user_role: BaseUserRole, service: UserRoleServiceDependency):
    return await service.add(user_role)


### importante tem de fazer
### adicionar validacao para quano o a request tiver parametros iguais ao do current_user
@router.put("/{user_role_id}", response_model=UserRole)
async def update_user_role(
    user_role_id: UUID, user_role: UpdateUserRole, service: UserRoleServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=user_role_id, schema=Userrole)


@router.delete("/{user_role_id}", status_code=204)
async def delete_user_role(user_role_id: UUID, service: UserRoleServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(user_role_id)
