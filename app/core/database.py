import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.settings import settings
from app.models import Base


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None  # type: ignore
        self._sessionmaker: async_sessionmaker | None = None  # type: ignore

    def init(self, database_url: str = settings.DATABASE_URL):
        self._engine = create_async_engine(database_url)
        self._sessionmaker = async_scoped_session(
            async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False),
            scopefunc=asyncio.current_task,
        )

    def session_factory(self):
        return self._sessionmaker

    def sync_create_all(self, engine):
        Base.metadata.create_all(engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)

    async def create_all_from_base(self, connection: AsyncConnection, base_model: declarative_base):
        await connection.run_sync(base_model.metadata.create_all)

    async def drop_all_from_base(self, connection: AsyncConnection, base_model: declarative_base):
        await connection.run_sync(base_model.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


async def get_db():
    async with sessionmanager.session() as session:
        yield session


async def get_session_factory():
    return sessionmanager.session_factory()
