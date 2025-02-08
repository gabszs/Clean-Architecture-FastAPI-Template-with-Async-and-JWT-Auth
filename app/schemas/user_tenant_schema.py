from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator

from app.core.exceptions import ValidationError
from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo
from uuid import UUID

class BaseUserTenant(BaseModel):
    user_id: UUID
    tenant_id: UUID
    description: Optional[str]

class UserTenant(BaseUserTenant, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)


class UpdateUserTenant(BaseModel):
    user_id: Optional[UUID]
    tenant_id: Optional[UUID]
    description: Optional[str]

class UserTenantList(FindModelResult):
    founds: List[UserTenant]
