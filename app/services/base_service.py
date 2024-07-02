from typing import Union
from uuid import UUID

from app.core.exceptions import AuthError
from app.models import User as UserModel
from app.repository.base_repository import BaseRepository
from app.schemas.base_schema import FindBase


class BaseService:
    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    async def validate_permission(self, id: Union[UUID, int], current_user: UserModel, admin: bool = False):
        if admin:
            if current_user.is_superuser is not True:
                raise AuthError(detail="Not enough permissions")
        else:
            if id != current_user.id:
                raise AuthError(detail="Not enough permissions")

    async def get_list(self, schema: FindBase, **kwargs):
        return await self._repository.read_by_options(schema, **kwargs)

    async def get_by_id(self, id: Union[UUID, int], **kwargs):
        return await self._repository.read_by_id(id, **kwargs)

    async def add(self, schema, **kwargs):
        return await self._repository.create(schema, **kwargs)

    async def patch(self, id: Union[UUID, int], schema, **kwargs):
        return await self._repository.update(id, schema, **kwargs)

    async def patch_attr(self, id: Union[UUID, int], attr: str, value, **kwargs):
        return await self._repository.update_attr(id, attr, value, **kwargs)

    async def put_update(self, id: Union[UUID, int], schema, **kwargs):
        return await self._repository.whole_update(id, schema, **kwargs)

    async def remove_by_id(self, id: Union[UUID, int], **kwargs):
        return await self._repository.delete_by_id(id, **kwargs)
