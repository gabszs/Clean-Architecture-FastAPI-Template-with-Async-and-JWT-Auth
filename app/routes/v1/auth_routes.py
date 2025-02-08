from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi import Header

from app.core.dependencies import AuthServiceDependency
from app.core.dependencies import CurrentTenantDependency
from app.core.dependencies import CurrentUserDependency
from app.schemas.auth_schema import SignIn
from app.schemas.auth_schema import SignInResponse
from app.schemas.auth_schema import SignUp
from app.schemas.user_schema import User as UserSchema
from app.schemas.user_schema import UserTenant
from app.schemas.user_schema import UserWithRoles


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-in", response_model=SignInResponse)
async def sign_in(user_info: SignIn, service: AuthServiceDependency):
    return await service.sign_in(user_info)


@router.post("/sign-up", status_code=201, response_model=UserSchema)
async def sign_up(user_info: SignUp, service: AuthServiceDependency):
    return await service.sign_up(user_info)


@router.post("/refresh-token", response_model=SignInResponse)
async def refresh_token(current_user: CurrentUserDependency, service: AuthServiceDependency):
    return await service.refresh_token(current_user)


@router.post("/tenant-token/", response_model=SignInResponse)
async def create_tenant_token(
    x_tenant_id: Annotated[UUID, Header()],
    current_user: CurrentUserDependency,
    service: AuthServiceDependency,
):
    return await service.generate_tenant_access_token(current_user, x_tenant_id)


@router.get("/tenant-token/", response_model=UserTenant)
async def get_tenant_token_data(
    current_tenant: CurrentTenantDependency,
):
    return current_tenant


@router.get("/me", response_model=UserWithRoles)
async def get_me(current_user: CurrentUserDependency):
    return current_user
