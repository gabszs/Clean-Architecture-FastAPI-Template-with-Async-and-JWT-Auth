from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator

from app.core.exceptions import ValidationError
from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo
from uuid import UUID

class BaseUserRole(BaseModel):
    user_id: UUID
    role_id: UUID
    description: Optional[str]


class UserRole(BaseUserRole, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)


class UpdateUserRole(BaseModel):
    user_id: Optional[UUID]
    role_id: Optional[UUID]
    description: Optional[str]


class UserRoleList(FindModelResult):
    founds: List[UserRole]
