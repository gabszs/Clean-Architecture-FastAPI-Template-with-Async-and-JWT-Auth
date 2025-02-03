from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict

from app.models.models_enums import DatabaseType
from app.models.models_enums import DatabaseType
from app.schemas.base_schema import FindModelResult
from app.schemas.base_schema import ModelBaseInfo


class BaseDatabase(BaseModel):
    name: str
    db_type: DatabaseType
    connection_string: str
    description: Optional[str]


class Database(BaseDatabase, ModelBaseInfo):
    model_config = ConfigDict(from_attributes=True)


class UpdateDatabase(BaseModel):
    name: Optional[str]
    db_type: Optional[DatabaseType]
    connection_string: Optional[str]
    description: Optional[str]


class DatabaseList(FindModelResult):
    founds: List[Database]
