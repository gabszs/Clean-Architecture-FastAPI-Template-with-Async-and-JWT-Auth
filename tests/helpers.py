from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.core.settings import settings
from app.models import User
from app.models.models_enums import UserRoles
from app.schemas.role_schema import Role
from app.schemas.tenant_schema import Tenant
from tests.factories import create_factory_users
from tests.factories import RoleFactory
from tests.factories import TenantFactory
from tests.schemas import UserModelSetup
from tests.schemas import UserSchemaWithHashedPassword


async def setup_tenant_data(
    session: AsyncSession, tenant_qty: int = 1, index: Optional[int] = None
) -> Union[List[Tenant], Tenant]:
    tenants = TenantFactory.create_batch(tenant_qty)
    tenant_list: List[Tenant] = []
    session.add_all(tenants)
    await session.commit()

    for tenant in tenants:
        await session.refresh(tenant)
        tenant_list.append(
            Tenant(
                name=tenant.name,
                slug=tenant.slug,
                id=tenant.id,
                created_at=tenant.created_at,
                updated_at=tenant.updated_at,
            )
        )

    if index is not None:
        return tenant_list[index]
    return tenant_list


async def setup_role_data(
    session: AsyncSession, role_qty: int = 1, index: Optional[int] = None
) -> Union[List[Role], Role]:
    tenant = await setup_tenant_data(session, index=0)
    tenant_id = tenant.id  # type: ignore

    roles = RoleFactory.create_batch(role_qty, tenant_id=tenant_id)
    role_list: List[Role] = []
    session.add_all(roles)
    await session.commit()

    for role in roles:
        await session.refresh(role)
        role_list.append(
            Role(
                tenant_id=role.tenant_id,
                name=role.name,
                description=role.description,
                id=role.id,
                created_at=role.created_at,
                updated_at=role.updated_at,
            )
        )

    if index is not None:
        return role_list[index]
    return role_list


def validate_datetime(data_string):
    try:
        datetime.strptime(data_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        try:
            datetime.strptime(data_string, "%Y-%m-%dT%H:%M:%S")
            return True
        except ValueError:
            return False


async def add_users_models(
    session: AsyncSession,
    users_qty: int = 1,
    user_role: UserRoles = UserRoles.BASE_USER,
    is_active=True,
    index: Optional[int] = None,
    get_model: bool = False,
) -> Union[List[Union[UserSchemaWithHashedPassword, User]], UserSchemaWithHashedPassword, User]:
    return_users: List[Union[UserSchemaWithHashedPassword, User]] = []
    users = create_factory_users(users_qty=users_qty, user_role=user_role, is_active=is_active)
    password_list = [factory_model.password for factory_model in users]
    for user in users:
        user.password = get_password_hash(user.password)
    session.add_all(users)
    await session.commit()
    for count, user in enumerate(users):
        await session.refresh(user)
        if get_model:
            return_users.append(user)
            continue
        return_users.append(
            UserSchemaWithHashedPassword(
                id=user.id,
                created_at=user.created_at,
                updated_at=user.updated_at,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                role=user.role,
                password=password_list[count],
                hashed_password=user.password,
            )
        )

    if index is not None:
        return return_users[index]
    return return_users


async def setup_users_data(
    session: AsyncSession, model_args: List[UserModelSetup], **kwargs
) -> List[UserSchemaWithHashedPassword]:  # type: ignore
    return_list: List[UserSchemaWithHashedPassword] = []
    for user_setup in model_args:
        user_list = await add_users_models(
            session, users_qty=user_setup.qty, user_role=user_setup.role, is_active=user_setup.is_active, **kwargs
        )
        return_list.append(*user_list)
    return return_list


async def token(client, session: AsyncSession, user):
    response = await client.post(
        f"{settings.base_auth_route}/sign-in", json={"email": user.email, "password": user.clean_password}
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


async def get_user_token(client: AsyncClient, user: UserSchemaWithHashedPassword) -> Dict[str, str]:
    response = await client.post(
        f"{settings.base_auth_route}/sign-in", json={"email": user.email, "password": user.password}
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


async def get_user_by_index(client, index: int = 0, token_header: Optional[str] = None):
    response = await client.get(f"{settings.base_users_url}/?ordering=username", headers=token_header)
    return response.json()["founds"][index]
