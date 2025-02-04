from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models import History
from app.repository.base_repository import BaseRepository


class HistoryRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, History)
