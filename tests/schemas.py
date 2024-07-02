from typing import Optional

from pydantic import BaseModel

from app.models.models_enums import UserRoles
from app.schemas.user_schema import User as UserSchema


class UserModelSetup(BaseModel):
    qty: int = 1
    is_active: bool = True
    role: UserRoles = UserRoles.BASE_USER


class UserSchemaWithHashedPassword(UserSchema):
    password: Optional[str] = None
    hashed_password: Optional[str] = None
