from typing import Annotated

from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.database import get_session_factory
from app.core.exceptions import AuthError
from app.core.security import JWTBearer
from app.core.settings import settings
from app.models import User
from app.repository.user_repository import UserRepository
from app.schemas.auth_schema import Payload
from app.schemas.base_schema import FindBase
from app.services.auth_service import AuthService
from app.services.user_service import UserService


async def get_user_service(session: Session = Depends(get_session_factory)):
    user_repository = UserRepository(session_factory=session)
    return UserService(user_repository)


async def get_current_user(token: str = Depends(JWTBearer()), service: UserService = Depends(get_user_service)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = await service.get_by_id(token_data.id)  # type: ignore
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


async def get_auth_service(session: Session = Depends(get_session_factory)):
    user_repository = UserRepository(session_factory=session)
    return AuthService(user_repository=user_repository)


FindQueryParameters = Annotated[FindBase, Depends()]
SessionDependency = Annotated[Session, Depends(get_db)]
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
CurrentActiveUserDependency = Annotated[User, Depends(get_current_active_user)]
