from typing import List
from urllib.parse import urlencode
from uuid import UUID

import pytest
from httpx import AsyncClient
from icecream import ic

from app.core.settings import settings
from tests.helpers import get_user_by_index
from tests.helpers import get_user_token
from tests.helpers import setup_users_data
from tests.helpers import validate_datetime
from tests.schemas import UserSchemaWithHashedPassword


async def get_token_user(client: AsyncClient, token_header: str) -> UserSchemaWithHashedPassword:
    user = await get_user_by_index(client, token_header=token_header)
    return UserSchemaWithHashedPassword(**user, password="", hashed_password="")


async def get_input_complete_list(
    client: AsyncClient, token_header: str, setup_users: List[UserSchemaWithHashedPassword]
) -> List[UserSchemaWithHashedPassword]:
    user = await get_token_user(client, token_header)
    setup_users.insert(0, user)
    return setup_users


@pytest.mark.anyio
async def test_get_all_users_should_return_200_OK_GET(
    session, client, default_username_search_options, batch_setup_users, moderator_user_token
):
    expected_lenght = (
        len(batch_setup_users) + 1
    )  # this plus one becouse of token_fixture, that adds one before this batch save
    setup_users = await setup_users_data(session=session, model_args=batch_setup_users)
    setup_users = await get_input_complete_list(client, moderator_user_token, setup_users)
    response = await client.get(
        f"{settings.base_users_url}/?{urlencode(default_username_search_options)}", headers=moderator_user_token
    )
    response_json = response.json()

    users_json = response_json["founds"]
    assert response.status_code == 200
    assert len(users_json) == expected_lenght
    assert response_json["search_options"] == default_username_search_options | {"total_count": expected_lenght}
    assert all(
        [
            user.username == users_json[count].get("username") and user.email == users_json[count].get("email")
            for count, user in enumerate(setup_users)
        ]
    )

    assert all([validate_datetime(user["created_at"]) for user in users_json])
    assert all([validate_datetime(user["updated_at"]) for user in users_json])


# # hard test
@pytest.mark.anyio
async def test_get_all_users_with_page_size_should_return_200_OK_GET(
    session, client, batch_setup_users, moderator_user_token
):
    query_find_parameters = {"ordering": "username", "page": 1, "page_size": 5}
    setup_users = await setup_users_data(session=session, model_args=batch_setup_users)
    setup_users = await get_input_complete_list(client, moderator_user_token, setup_users)

    response = await client.get(
        f"{settings.base_users_url}/?{urlencode(query_find_parameters)}", headers=moderator_user_token
    )
    response_json = response.json()

    assert response.status_code == 200
    assert all(
        [
            user.username == response_json["founds"][count].get("username")
            and user.email == response_json["founds"][count].get("email")
            for count, user in enumerate(setup_users[: query_find_parameters["page_size"]])
        ]
    )
    assert len(response_json["founds"]) == 5
    assert response_json["search_options"] == query_find_parameters | {"total_count": 5}
    assert all([validate_datetime(user["created_at"]) for user in response_json["founds"]])
    assert all([validate_datetime(user["updated_at"]) for user in response_json["founds"]])


# hard test
@pytest.mark.anyio
async def test_get_all_users_with_pagination_should_return_200_OK_GET(
    session, client, batch_setup_users, moderator_user_token
):
    page_size = 3
    page = 2
    ordering = "username"
    query_find_parameters = {"ordering": ordering, "page": page, "page_size": page_size}
    setup_users = await setup_users_data(session=session, model_args=batch_setup_users)
    setup_users = await get_input_complete_list(client, moderator_user_token, setup_users)

    response = await client.get(
        f"{settings.base_users_url}/?{urlencode(query_find_parameters)}", headers=moderator_user_token
    )
    response_json = response.json()

    assert response.status_code == 200
    assert all(
        [
            user.username == response_json["founds"][count].get("username")
            and user.email == response_json["founds"][count].get("email")
            for count, user in enumerate(setup_users[page_size : page_size * page])
        ]
    )
    assert len(response_json["founds"]) == query_find_parameters["page_size"]
    assert response_json["search_options"] == query_find_parameters | {
        "total_count": query_find_parameters["page_size"]
    }
    assert all([validate_datetime(user["created_at"]) for user in response_json["founds"]])
    assert all([validate_datetime(user["updated_at"]) for user in response_json["founds"]])


# hard test
@pytest.mark.anyio
async def test_get_user_by_id_should_return_200_OK_GET(session, client, moderator_user, batch_setup_users):
    moderator_token = await get_user_token(client, moderator_user)
    response = await client.get(f"{settings.base_users_url}/{moderator_user.id}", headers=moderator_token)
    response_json = response.json()

    assert response.status_code == 200
    assert UUID(response_json["id"]) == moderator_user.id
    assert response_json["is_active"] is True
    assert response_json["role"] == moderator_user.role
    assert response_json["email"] == moderator_user.email
    assert response_json["username"] == moderator_user.username
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_get_user_by_id_should_return_404_NOT_FOUND_GET(session, random_uuid, client, moderator_user_token):
    response = await client.get(f"{settings.base_users_url}/{random_uuid}", headers=moderator_user_token)

    assert response.status_code == 404
    assert response.json() == {"detail": f"id not found: {random_uuid}"}


@pytest.mark.anyio
async def test_create_normal_user_should_return_422_unprocessable_entity_POST(client):
    response = await client.post(
        f"{settings.base_users_url}/",
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_normal_user_should_return_201_POST(client, session, factory_user):
    response = await client.post(
        f"{settings.base_users_url}/",
        json={"email": factory_user.email, "username": factory_user.username, "password": factory_user.password},
    )
    response_json = response.json()

    assert response.status_code == 201
    assert UUID(response_json["id"])
    assert response_json["email"] == factory_user.email
    assert response_json["username"] == factory_user.username
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_create_normal_user_should_return_409_email_already_registered_POST(client, session, normal_user):
    response = await client.post(
        f"{settings.base_users_url}/",
        json={"email": normal_user.email, "username": "different_username", "password": normal_user.password},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.anyio
async def test_create_normal_user_should_return_409_username_already_registered_POST(client, session, normal_user):
    response = await client.post(
        f"{settings.base_users_url}/",
        json={"email": "different@email.com", "username": normal_user.username, "password": normal_user.password},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Username already registered"}


@pytest.mark.anyio
async def test_disable_user_should_return_200_OK_DELETE(session, client, normal_user, moderator_user_token):
    token = await get_user_token(client, normal_user)
    response = await client.delete(f"{settings.base_users_url}/disable/{normal_user.id}", headers=token)
    response_json = response.json()
    modified_user = await get_user_by_index(client, 0, token_header=moderator_user_token)

    assert response.status_code == 200
    assert response_json == {"detail": "User has been desabled successfully"}
    assert normal_user.is_active is True
    assert modified_user["is_active"] is False
    assert modified_user["email"] == normal_user.email
    assert modified_user["username"] == normal_user.username
    assert modified_user["id"] == str(normal_user.id)


@pytest.mark.anyio
async def test_disable_different_user_should_return_403_FORBIDDEN_DELETE(
    session, client, normal_user, normal_user_token
):
    response = await client.delete(f"{settings.base_users_url}/disable/{normal_user.id}", headers=normal_user_token)
    response_json = response.json()

    assert response.status_code == 403
    assert response_json == {"detail": "Not enough permissions"}


@pytest.mark.anyio
async def test_enable_user_user_should_return_200_OK_PATCH(session, client, disable_normal_user, moderator_user_token):
    token = await get_user_token(client, disable_normal_user)
    response = await client.patch(f"{settings.base_users_url}/enable_user/{disable_normal_user.id}", headers=token)
    response_json = response.json()
    modified_user = await get_user_by_index(client, 0, token_header=moderator_user_token)

    assert response.status_code == 200
    assert response_json == {"detail": "User has been enabled successfully"}
    assert disable_normal_user.is_active is False
    assert modified_user["is_active"] is True
    assert modified_user["email"] == disable_normal_user.email
    assert modified_user["username"] == disable_normal_user.username
    assert modified_user["id"] == str(disable_normal_user.id)


@pytest.mark.anyio
async def test_enable_user_different_user_should_return_403_FORBIDDEN_PATCH(
    session, client, normal_user, normal_user_token
):
    response = await client.patch(f"{settings.base_users_url}/enable_user/{normal_user.id}", headers=normal_user_token)
    response_json = response.json()
    assert response.status_code == 403
    assert response_json == {"detail": "Not enough permissions"}


@pytest.mark.anyio
async def test_delete_user_should_return_200_OK_DELETE(session, client, normal_user, admin_user_token):
    response = await client.delete(f"{settings.base_users_url}/{normal_user.id}", headers=admin_user_token)
    get_users_response = await client.get(f"{settings.base_users_url}/?offset=0&limit=100", headers=admin_user_token)

    assert response.status_code == 204
    assert get_users_response.status_code == 200
    assert len(get_users_response.json()["founds"]) == 1


@pytest.mark.anyio
async def test_delete_different_authorization_should_return_403_FORBIDDEN_DELETE(
    session, client, normal_user, normal_user_token
):
    response = await client.delete(f"{settings.base_users_url}/{normal_user.id}", headers=normal_user_token)
    response_json = response.json()
    assert response.status_code == 403
    assert response_json == {"detail": "Not enough permissions"}


@pytest.mark.anyio
async def test_put_user_should_return_200_OK_PUT(session, client, factory_user, normal_user):
    token = await get_user_token(client, normal_user)
    different_user = {
        "email": factory_user.email,
        "username": factory_user.username,
        "is_active": False,
    }

    response = await client.put(f"{settings.base_users_url}/{normal_user.id}", headers=token, json=different_user)
    response_json = response.json()

    assert response.status_code == 200
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])
    assert all([response_json[key] == value for key, value in different_user.items()])


@pytest.mark.anyio
async def test_put_user_with_admin_should_return_200_OK_PUT(
    session, client, factory_user, normal_user, admin_user_token
):
    different_user = {
        "email": factory_user.email,
        "username": factory_user.username,
        "is_active": False,
    }

    response = await client.put(
        f"{settings.base_users_url}/{normal_user.id}", headers=admin_user_token, json=different_user
    )
    response_json = response.json()

    assert response.status_code == 200
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])
    assert all([response_json[key] == value for key, value in different_user.items()])


@pytest.mark.anyio
async def test_put_user_should_return_403_FORBIDDEN_PUT(session, client, factory_user, normal_user, moderator_user):
    token = await get_user_token(client, normal_user)

    different_user = {
        "email": factory_user.email,
        "username": factory_user.username,
        "is_active": False,
        "is_superuser": True,
    }

    response = await client.put(f"{settings.base_users_url}/{moderator_user.id}", headers=token, json=different_user)

    assert response.json() == {"detail": "Not enough permissions"}
    assert response.status_code == 403


ic
