from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseRole(BaseModel):
    tenant_id: UUID
    name: str
    description: Optional[str]


class Role(BaseRole, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)


class UpdateRole(BaseModel):
    name: Optional[str]
    description: Optional[str]


class RoleList(FindModelResult):
    founds: List[Role]
