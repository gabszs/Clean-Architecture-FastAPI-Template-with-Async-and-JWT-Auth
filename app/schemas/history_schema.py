from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict

from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseHistory(BaseModel):
    database_id: UUID
    name: Optional[str]
    schemas: Optional[str]


class History(BaseHistory, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)


class UpdateHistory(BaseModel):
    database_id: Optional[UUID]
    name: Optional[str]
    schemas: Optional[str]


class HistoryList(FindModelResult):
    founds: List[History]
