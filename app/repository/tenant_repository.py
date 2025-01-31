from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.models import Tenant
from app.repository.base_repository import BaseRepository


class TenantRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Tenant)
