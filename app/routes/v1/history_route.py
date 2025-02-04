from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from app.core.dependencies import CurrentUserDependency
from app.core.dependencies import FindBase
from app.core.dependencies import HistoryServiceDependency
from app.schemas.history_schema import BaseHistory
from app.schemas.history_schema import History
from app.schemas.history_schema import HistoryList
from app.schemas.history_schema import UpdateHistory

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/", response_model=HistoryList)
async def get_history_list(
    service: HistoryServiceDependency, current_user: CurrentUserDependency, find_query: FindBase = Depends()
):
    return await service.get_list(find_query)


@router.get("/{History_id}", response_model=History)
async def get_history_by_id(History_id: UUID, service: HistoryServiceDependency, current_user: CurrentUserDependency):
    return await service.get_by_id(History_id)


@router.post("/", status_code=201, response_model=History)
async def create_history(history: BaseHistory, service: HistoryServiceDependency):
    return await service.add(history)


@router.put("/{History_id}", response_model=History)
async def update_history(
    History_id: UUID, History: UpdateHistory, service: HistoryServiceDependency, current_user: CurrentUserDependency
):
    return await service.patch(id=History_id, schema=History)


@router.delete("/{History_id}", status_code=204)
async def delete_user(History_id: UUID, service: HistoryServiceDependency, current_user: CurrentUserDependency):
    await service.remove_by_id(History_id)
