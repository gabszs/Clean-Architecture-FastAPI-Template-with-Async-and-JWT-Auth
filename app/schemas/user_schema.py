from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr

from app.schemas.base_schema import AllOptional
from app.schemas.base_schema import FindBase
from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo
from app.schemas.tenant_schema import Tenant
from app.schemas.user_role_schema import BaseUserRole
from app.schemas.user_tenant_schema import BaseUserTenant


class BaseUser(BaseModel):
    email: EmailStr
    username: str


class BaseUserWithPassword(BaseUser):
    password: str


class User(BaseUser, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)
    is_active: bool


class UserTenant(User):
    tenant: Tenant


class UserWithRoles(User):
    tenants: List[Optional[BaseUserTenant]]
    roles: List[Optional[BaseUserRole]]


class OptionalUser(User, metaclass=AllOptional):
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    ...


class UpsertUser(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    is_active: Optional[bool]


class FindUserResult(FindModelResult):
    founds: List[User]


class UserWithCleanPassword(BaseUserWithPassword):
    clean_password: str
