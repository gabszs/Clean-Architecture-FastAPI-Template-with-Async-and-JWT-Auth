from typing import Annotated

from fastapi import Depends
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.database import get_session_factory
from app.core.exceptions import AuthError
from app.core.exceptions import NotFoundError
from app.core.security import JWTBearer
from app.core.settings import settings
from app.models import Tenant
from app.models import User
from app.repository import RoleRepository
from app.repository import TenantRepository
from app.repository import UserRepository
from app.repository import UserRoleRepository
from app.repository import UserTenantRepository
from app.schemas.auth_schema import Payload
from app.schemas.auth_schema import TenantPayload
from app.schemas.base_schema import FindBase
from app.schemas.tenant_schema import Tenant as TenantSchema
from app.schemas.user_schema import User as UserSchema
from app.schemas.user_schema import UserTenant
from app.services import AuthService
from app.services import RoleService
from app.services import TenantService
from app.services import UserRoleService
from app.services import UserService
from app.services import UserTenantService


async def get_user_service(session: Session = Depends(get_session_factory)):
    user_repository = UserRepository(session_factory=session)
    tenant_repository = TenantRepository(session_factory=session)
    return UserService(user_repository, tenant_repository)


async def get_tenant_service(session: Session = Depends(get_session_factory)):
    tenant_repository = TenantRepository(session_factory=session)
    return TenantService(tenant_repository=tenant_repository)


async def get_current_user(token: str = Depends(JWTBearer()), service: UserService = Depends(get_user_service)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = Payload(**payload)
        current_user: User = await service.get_by_id(token_data.id, eager=True, use_select=True)  # type: ignore
    except (JWTError, ValidationError, NotFoundError):
        raise AuthError(detail="Could not validate credentials")
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


async def get_auth_service(session: Session = Depends(get_session_factory)):
    user_repository = UserRepository(session_factory=session)
    tenant_repository = TenantRepository(session_factory=session)
    return AuthService(user_repository=user_repository, tenant_repository=tenant_repository)


async def get_tenant_token(
    token: str = Depends(JWTBearer()), session: Session = Depends(get_session_factory)
) -> UserTenant:
    user_repository: UserRepository = UserRepository(session_factory=session)
    tenant_repository: TenantRepository = TenantRepository(session_factory=session)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TenantPayload(**payload)
        current_user: User = await user_repository.read_by_id(token_data.id, eager=True, use_select=True)  # type: ignore
        tenant: Tenant = await tenant_repository.read_by_id(token_data.tenant_id)

    except (JWTError, ValidationError, NotFoundError):
        raise AuthError(detail="Could not validate credentials")
    if not current_user:
        raise AuthError(detail="User not found")
    tenant_schema: TenantSchema = TenantSchema.model_validate(tenant)
    current_user_schema: UserSchema = UserSchema.model_validate(current_user)
    return UserTenant(**current_user_schema.model_dump(), tenant=tenant_schema)


async def get_role_service(session: Session = Depends(get_session_factory)):
    role_repository = RoleRepository(session_factory=session)
    return RoleService(role_repository=role_repository)


async def get_user_role_service(session: Session = Depends(get_session_factory)):
    user_role_repository = UserRoleRepository(session_factory=session)
    return UserRoleService(user_role_repository=user_role_repository)


async def get_user_tenant_service(session: Session = Depends(get_session_factory)):
    user_tenant_repository = UserTenantRepository(session_factory=session)
    return UserTenantService(user_tenant_repository=user_tenant_repository)


FindQueryParameters = Annotated[FindBase, Depends()]
SessionDependency = Annotated[Session, Depends(get_db)]
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]
CurrentTenantDependency = Annotated[UserTenant, Depends(get_tenant_token)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
TenantServiceDependency = Annotated[TenantService, Depends(get_tenant_service)]
RoleServiceDependency = Annotated[RoleService, Depends(get_role_service)]
UserRoleServiceDependency = Annotated[RoleService, Depends(get_user_role_service)]
CurrentActiveUserDependency = Annotated[User, Depends(get_current_active_user)]
UserTenantServiceDependency = Annotated[UserTenantService, Depends(get_user_tenant_service)]
