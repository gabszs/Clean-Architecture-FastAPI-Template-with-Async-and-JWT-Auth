from datetime import datetime
from typing import Annotated
from typing import Any
from typing import List
from typing import Optional
from typing import Union
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic import ValidationInfo
from pydantic._internal._model_construction import ModelMetaclass

from app.core.exceptions import ValidationError
from app.core.settings import settings


class Message(BaseModel):
    detail: str


class NoContent(BaseModel):
    pass


class AllOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class ModelBaseInfo(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class FindBase(BaseModel):
    ordering: Optional[str] = settings.ORDERING
    page: Annotated[int, Field(gt=0)] = settings.PAGE
    page_size: Optional[Union[int, str]] = settings.PAGE_SIZE

    @field_validator("page_size")
    @classmethod
    def page_size_field_validator(cls, value: Union[str, int], info: ValidationInfo):
        try:
            input = int(value)
            if input < 0:
                raise ValidationError("Page size must be a positive integer")
            return input
        except Exception as _:
            if value != "all":
                raise ValidationError("Page size must be 'all' or a positive integer")
            return value


class SearchOptions(FindBase):
    total_count: Optional[int]


class FindResult(BaseModel):
    founds: Optional[List]
    search_options: Optional[SearchOptions]


class FindDateRange(BaseModel):
    created_at__lt: str
    created_at__lte: str
    created_at__gt: str
    created_at__gte: str


class FindModelResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    founds: List[Any]
    search_options: SearchOptions


class Blank(BaseModel):
    pass
