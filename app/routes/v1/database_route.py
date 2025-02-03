from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import DatabaseServiceDependency
from app.core.dependencies import FindBase
from app.schemas.database_schema import BaseDatabase
from app.schemas.database_schema import Database
from app.schemas.database_schema import DatabaseList
from app.schemas.database_schema import UpdateDatabase

router = APIRouter(prefix="/database", tags=["database"])


@router.get("/", response_model=DatabaseList)
async def get_database_list(
    service: DatabaseServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{database_id}", response_model=Database)
async def get_database_by_id(
    database_id: UUID, service: DatabaseServiceDependency, current_user: CurrentUserDependency
):
    return await service.get_by_id(database_id)


@router.post("/", status_code=201, response_model=Database)
async def create_database(user: BaseDatabase, service: DatabaseServiceDependency):
    return await service.add(user)


@router.put("/{database_id}", response_model=Database)
async def update_database(
    database_id: UUID, Database: UpdateDatabase, service: DatabaseServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=database_id, schema=Database)


@router.delete("/{database_id}", status_code=204)
async def delete_user(database_id: UUID, service: DatabaseServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(database_id)
