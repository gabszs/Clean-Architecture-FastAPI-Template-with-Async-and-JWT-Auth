from contextlib import AbstractAsyncContextManager
from typing import Any
from typing import Callable
from typing import Union
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestError
from app.core.exceptions import DuplicatedError
from app.core.exceptions import NotFoundError
from app.core.exceptions import ValidationError
from app.core.settings import Settings
from app.schemas.base_schema import FindBase

settings = Settings()


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[Session]], model) -> None:
        self.session_factory = session_factory
        self.model = model

    async def get_order_by(self, schema):
        try:
            return (
                getattr(self.model, schema.ordering[1:]).desc()
                if schema.ordering.startswith("-")
                else getattr(self.model, schema.ordering).asc()
            )
        except AttributeError:
            raise ValidationError(f"Unprocessable Entity, attribute '{schema.ordering}' does not exist")

    async def get_model_by_id(self, session: AsyncSession, id: Union[UUID, int], not_unique_pk: bool = False):
        if not_unique_pk:
            return await session.scalar(select(self.model).where(self.model.id == id))
        return await session.get(self.model, id)

    def get_compiled_stmt(self, stmt: select) -> str:
        return str(stmt.compile(compile_kwargs={"literal_binds": True}))

    async def read_by_options(self, schema: FindBase, eager: bool = False, unique: bool = False):
        async with self.session_factory() as session:  # type: ignore
            order_query = await self.get_order_by(schema)
            stmt = select(self.model).order_by(order_query)
            if eager:
                for eager_relation in getattr(self.model, "eagers", []):
                    stmt = stmt.options(joinedload(getattr(self.model, eager_relation)))
            if schema.page_size != "all":
                stmt = stmt.offset((schema.page - 1) * (schema.page_size)).limit(int(schema.page_size))  # type: ignore

            # compiled_stmt = str(stmt.compile(compile_kwargs={"literal_binds": True})) -> exibe a query

            query = await session.execute(stmt)
            if unique:
                result = query.unique()
            result = query.scalars().all()
            return {
                "founds": result,
                "search_options": {
                    "page": schema.page,
                    "page_size": schema.page_size,
                    "ordering": schema.ordering,
                    "total_count": len(result),
                },
            }

    async def read_by_id(self, id: Union[UUID, int], not_unique_pk: bool = False):
        async with self.session_factory() as session:
            result = await self.get_model_by_id(session, id, not_unique_pk)
            if not result:
                raise NotFoundError(detail=f"id not found: {id}")
            return result

    async def read_by_email(self, email: EmailStr, unique: bool = False):
        async with self.session_factory() as session:
            stmt = select(self.model).where(self.model.email == email)
            result = await session.execute(stmt)
            if unique:
                result = result.unique()
            user = result.scalars().all()

            return user

    async def create(self, schema):
        async with self.session_factory() as session:
            model = self.model(**schema.model_dump())
            try:
                session.add(model)
                await session.commit()
                await session.refresh(model)

            except IntegrityError as _:
                raise DuplicatedError(detail=f"{self.model.__tablename__.capitalize()[:-1]} already registered")
            except Exception as error:
                raise BadRequestError(str(error))
            return model

    async def update(self, id: Union[UUID, int], schema, not_unique_pk: bool = True):
        async with self.session_factory() as session:
            schema = schema.model_dump()
            result = await self.get_model_by_id(session, id, not_unique_pk)

            if not result:
                raise NotFoundError(detail=f"id not found: {id}")

            if schema == {attr: getattr(result, attr) for attr in schema.keys()}:
                raise BadRequestError(detail="No changes detected")

            stmt = update(self.model).where(self.model.id == id).values(**schema)
            try:
                await session.execute(stmt)
                await session.commit()
                await session.refresh(result)
                return result
            except IntegrityError as e:
                error_message = ":".join(str(e.orig).replace("\n", " ").split(":")[1:])
                raise DuplicatedError(detail=error_message)

    async def update_attr(self, id: Union[UUID, int], column: str, value: Any, not_unique_pk: bool = False):
        async with self.session_factory() as session:
            result = await self.get_model_by_id(session, id, not_unique_pk)
            if not result:
                raise NotFoundError(detail=f"id not found: {id}")
            if value == getattr(result, column):
                raise BadRequestError(detail="No changes detected")

            stmt = update(self.model).where(self.model.id == id).values({column: value})
            try:
                await session.execute(stmt)
                await session.commit()
                await session.refresh(result)
                return result
            except IntegrityError as e:
                error_message = ":".join(str(e.orig).replace("\n", " ").split(":")[1:])
                raise DuplicatedError(detail=error_message)

    # BROKEN
    async def whole_update(self, id: Union[UUID, int], schema):
        async with self.session_factory() as session:
            await session.query(self.model).filter(self.model.id == id).update(schema.model_dump())
            await session.commit()
            return self.read_by_id(id)

    async def delete_by_id(self, id: Union[UUID, int], not_unique_pk: bool = False):
        async with self.session_factory() as session:
            result = await self.get_model_by_id(session, id, not_unique_pk)
            if not result:
                raise NotFoundError(detail=f"not found id: {id}")
            await session.delete(result)
            await session.commit()
