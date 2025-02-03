from app.repository import DatabaseRepository
from app.services.base_service import BaseService


class DatabaseService(BaseService):
    def __init__(self, database_repository: DatabaseRepository):
        self.database_repository = database_repository
        super().__init__(database_repository)
