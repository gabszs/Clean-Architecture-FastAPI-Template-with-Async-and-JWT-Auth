from datetime import timedelta
from typing import List
from uuid import UUID

from app.core.exceptions import AuthError
from app.core.exceptions import InvalidCredentials
from app.core.exceptions import NotFoundError
from app.core.security import create_access_token
from app.core.security import get_password_hash
from app.core.security import verify_password
from app.core.settings import settings
from app.models import User
from app.repository import TenantRepository
from app.repository import UserRepository
from app.schemas.auth_schema import Payload
from app.schemas.auth_schema import SignIn
from app.schemas.auth_schema import SignInResponse
from app.schemas.auth_schema import SignUp
from app.schemas.auth_schema import TenantPayload
from app.schemas.user_schema import BaseUserWithPassword
from app.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository, tenant_repository: TenantRepository):
        self.user_repository = user_repository
        self._tenant_repository = tenant_repository
        super().__init__(user_repository)

    async def sign_in(self, sign_in_info: SignIn) -> SignInResponse:
        user: List[User] = await self.user_repository.read_by_email(email=sign_in_info.email, unique=True)
        if len(user) < 1:
            raise InvalidCredentials(detail="Incorrect email or user not exist")
        found_user: User = user[0]

        if not verify_password(sign_in_info.password, found_user.password):
            raise InvalidCredentials(detail="Incorrect password")

        delattr(found_user, "password")

        payload = Payload(id=str(found_user.id), email=found_user.email, username=found_user.username)
        token_lifespan = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        sign_in_result = SignInResponse(access_token=access_token, expiration=expiration_datetime, user_info=found_user)
        return sign_in_result

    async def sign_up(self, user_info: SignUp) -> User:
        user = BaseUserWithPassword(**user_info.model_dump(exclude_none=True))
        user.password = get_password_hash(user_info.password)
        created_user = await self.user_repository.create(user)
        delattr(created_user, "password")
        return created_user

    async def refresh_token(self, current_user: User) -> SignInResponse:
        payload = Payload(id=str(current_user.id), email=current_user.email, username=current_user.username)
        token_lifespan = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        sign_in_result = SignInResponse(
            access_token=access_token, expiration=expiration_datetime, user_info=current_user
        )
        return sign_in_result

    async def generate_tenant_access_token(self, current_user: User, tenant_id: UUID):
        if current_user.tenant_id != tenant_id:
            raise AuthError(detail="User does not have access to this Tenant")

        tenant = await self._tenant_repository.read_by_id(tenant_id)
        if not tenant:
            raise NotFoundError(detail="Tenant does not exists")

        payload = TenantPayload(
            id=str(current_user.id),
            email=current_user.email,
            username=current_user.username,
            tenant_id=str(tenant.id),
        )

        token_lifespan = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
        sign_in_result = SignInResponse(
            access_token=access_token, expiration=expiration_datetime, user_info=current_user
        )
        return sign_in_result


#  payload = Payload(id=str(found_user.id), email=found_user.email, username=found_user.username)
#         token_lifespan = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token, expiration_datetime = create_access_token(payload.model_dump(), token_lifespan)
#         sign_in_result = SignInResponse(access_token=access_token, expiration=expiration_datetime, user_info=found_user)
#         return sign_in_result
