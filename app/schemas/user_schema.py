from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field

from app.models.models_enums import UserRoles
from app.schemas.base_schema import AllOptional
from app.schemas.base_schema import FindBase
from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseUser(BaseModel):
    email: EmailStr = Field(default="test@test.com")
    username: str = Field(default="test")


class BaseUserWithPassword(BaseUser):
    password: str = Field(default="test")


class User(BaseUser, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)

    is_active: bool
    role: UserRoles


class OptionalUser(User, metaclass=AllOptional):
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    ...


class UpsertUser(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    is_active: Optional[bool]


class FindUserResult(FindModelResult):
    data: List[User]


class UserWithCleanPassword(BaseUserWithPassword):
    clean_password: str
