from typing import Union
from uuid import UUID

from slugify import slugify  # type: ignore

from app.repository import TenantRepository
from app.schemas.tenant_schema import BaseTenant
from app.schemas.tenant_schema import TenantWithSlug
from app.services.base_service import BaseService


class TenantService(BaseService):
    def __init__(self, tenant_repository: TenantRepository):
        self.tenant_repository = tenant_repository
        super().__init__(tenant_repository)

    async def add(self, schema: BaseTenant, **kwargs):
        slug = slugify(schema.name)
        tenant_schema = TenantWithSlug(name=schema.name, slug=slug)

        return await self._repository.create(tenant_schema, **kwargs)

    async def patch(self, id: Union[UUID, int], schema: BaseTenant, **kwargs):
        slug = slugify(schema.name)
        tenant_schema = TenantWithSlug(name=schema.name, slug=slug)

        return await self._repository.update(id, tenant_schema, **kwargs)
