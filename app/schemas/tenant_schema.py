from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator
from slugify import slugify  # type: ignore

from app.core.exceptions import ValidationError
from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseTenant(BaseModel):
    name: str


class TenantWithSlug(BaseTenant):
    slug: str


class Tenant(BaseTenant, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)

    slug: str

    @field_validator("slug")
    def validate_slug(cls, value: str) -> str:
        if value != slugify(value):
            raise ValidationError(detail="The value is not a valid slug")
        return value


class UpsertTenant(BaseModel):
    name: Optional[str]


class TenantList(FindModelResult):
    founds: List[Tenant]
