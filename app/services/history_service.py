from app.repository import HistoryRepository
from app.services.base_service import BaseService


class HistoryService(BaseService):
    def __init__(self, history_repository: HistoryRepository):
        self.history_repository = history_repository
        super().__init__(history_repository)
