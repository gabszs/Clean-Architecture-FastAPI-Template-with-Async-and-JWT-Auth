from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindBase
from app.core.dependencies import UserServiceDependency
from app.core.security import authorize
from app.models.models_enums import UserRoles
from app.schemas.base_schema import Message
from app.schemas.user_schema import BaseUserWithPassword
from app.schemas.user_schema import FindUserResult
from app.schemas.user_schema import UpsertUser
from app.schemas.user_schema import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=FindUserResult)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN])
async def get_user_list(
    service: UserServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{user_id}", response_model=User)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN], allow_same_id=True)
async def get_user_by_id(user_id: UUID, service: UserServiceDependency, current_user: CurrentUserDependency):
    return await service.get_by_id(user_id)


@router.post("/", status_code=201, response_model=User)
async def create_user(user: BaseUserWithPassword, service: UserServiceDependency):
    return await service.add(user)


### importante tem de fazer
### adicionar validacao para quano o a request tiver parametros iguais ao do current_user
@router.put("/{user_id}", response_model=User)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN], allow_same_id=True)
async def update_user(
    user_id: UUID, user: UpsertUser, service: UserServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=user_id, schema=user, current_user=current_user)


@router.patch("/enable_user/{user_id}", response_model=Message)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN], allow_same_id=True)
async def enabled_user(user_id: UUID, service: UserServiceDependency, current_user: CurrentUserDependency):
    await service.patch_attr(id=user_id, attr="is_active", value=True, current_user=current_user)
    return Message(detail="User has been enabled successfully")


@router.delete("/disable/{user_id}", response_model=Message)
@authorize(role=[UserRoles.MODERATOR, UserRoles.ADMIN], allow_same_id=True)
async def disable_user(user_id: UUID, service: UserServiceDependency, current_user: CurrentUserDependency):
    await service.patch_attr(id=user_id, attr="is_active", value=False, current_user=current_user)
    return Message(detail="User has been desabled successfully")


@router.delete("/{user_id}", status_code=204)
@authorize(role=[UserRoles.ADMIN])
async def delete_user(user_id: UUID, service: UserServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(user_id)
