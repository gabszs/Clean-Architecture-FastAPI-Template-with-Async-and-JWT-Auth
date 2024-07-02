from typing import Union
from uuid import UUID

from app.core.security import get_password_hash
from app.models import User as UserModel
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import BaseUserWithPassword
from app.services.base_service import BaseService
from app.services.base_service import FindBase


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def get_list(self, schema: FindBase):  # type: ignore
        return await self._repository.read_by_options(schema, unique=True)

    async def add(self, user_schema: BaseUserWithPassword):  # type: ignore
        user_schema.password = get_password_hash(user_schema.password)
        created_user = await self._repository.create(user_schema)
        delattr(created_user, "password")
        return created_user

    # will come here later, but for now only admin can touch this method
    # async def remove_by_id(self, id: Union[UUID, int], current_user: UserModel):
    #     return await self._repository.delete_by_id(id)

    async def patch(self, id: Union[UUID, int], schema, current_user: UserModel):  # type: ignore
        return await self._repository.update(id, schema)

    async def patch_attr(self, id: Union[UUID, int], attr: str, value, current_user: UserModel):  # type: ignore
        return await self._repository.update_attr(id, attr, value)
