from uuid import UUID

import pytest
from freezegun import freeze_time
from icecream import ic

from app.core.settings import settings
from tests.helpers import validate_datetime


@pytest.mark.anyio
async def test_get_token_should_return_200_OK_POST(client, session, normal_user):
    response = await client.post(
        f"{settings.base_auth_route}/sign-in", json={"email": normal_user.email, "password": normal_user.clean_password}
    )
    response_json = response.json()
    user_info = response_json["user_info"]

    assert response.status_code == 200
    assert "access_token" in response_json
    assert validate_datetime(response_json["expiration"])

    assert UUID(user_info["id"])
    assert user_info["email"] == normal_user.email
    assert user_info["username"] == normal_user.username
    assert user_info["is_active"] is True
    assert validate_datetime(user_info["created_at"])
    assert validate_datetime(user_info["updated_at"])


@pytest.mark.anyio
async def test_auth_token_expired_after_time_should_return_403_FORBIDDEN_POST(client, session, normal_user):
    overtime_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1

    with freeze_time("2023-12-28 12:00:00"):
        response = await client.post(
            f"{settings.base_auth_route}/sign-in",
            json={"email": normal_user.email, "password": normal_user.clean_password},
        )

        assert response.status_code == 200
        token = response.json()["access_token"]
        token_header = {"Authorization": f"Bearer {token}"}

    with freeze_time(f"2023-12-28 12:{overtime_minutes}:00"):
        response = await client.get(f"{settings.base_auth_route}/me", headers=token_header)

        assert response.status_code == 403
        assert response.json() == {"detail": "Invalid token or expired token"}


@pytest.mark.anyio
async def test_auth_token_inexistent_user_should_return_401_INVALIDCREDENTIALS_POST(client, session):
    response = await client.post(
        f"{settings.base_auth_route}/sign-in", json={"email": "email@test.com", "password": "test_password"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or user not exist"}


@pytest.mark.anyio
async def test_auth_token_wrong_user_should_return_401_INVALIDCREDENTIALS_POST(client, session, normal_user):
    response = await client.post(
        f"{settings.base_auth_route}/sign-in", json={"email": normal_user.email, "password": "wrong_password"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}


@pytest.mark.anyio
async def test_auth_get_me_route_without_token_should_return_403_FORBIDDEN_GET(client, session):
    response = await client.get(f"{settings.base_auth_route}/me", headers={"Authorization": ""})

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


# Hard code pra krl kkkkk, nao quero fazer outras chamada na api para pegar os dados
# ou refatorar as fixtures para retornar com atributo de user + token_header
@pytest.mark.anyio
async def test_auth_get_me_should_return_200_OK_GET(client, session, base_user_token):
    response = await client.get(f"{settings.base_auth_route}/me", headers=base_user_token)
    response_json = response.json()

    ic(response_json)
    assert response.status_code == 200
    assert UUID(response_json["id"])
    assert response_json["is_active"] is True
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])
    assert len(response_json["tenants"]) == 0
    assert len(response_json["roles"]) == 0


@pytest.mark.anyio
async def test_auth_token_expired_after_dont_refresh_should_return_403_FORBIDDEN_POST(client, session, normal_user):
    overtime_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1

    with freeze_time("2023-12-28 12:00:00"):
        response = await client.post(
            f"{settings.base_auth_route}/sign-in",
            json={"email": normal_user.email, "password": normal_user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        token_header = {"Authorization": f"Bearer {token}"}

    with freeze_time(f"2023-12-28 12:{overtime_minutes}:00"):
        response = await client.post(f"{settings.base_auth_route}/refresh-token", headers=token_header)

        ic(response)
        assert response.status_code == 403
        assert response.json() == {"detail": "Invalid token or expired token"}


@pytest.mark.anyio
async def test_refresh_token_should_return_200_OK_POST(client, session, normal_user):
    overtime_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES - 1

    with freeze_time("2023-12-28 12:00:00"):
        response = await client.post(
            f"{settings.base_auth_route}/sign-in",
            json={"email": normal_user.email, "password": normal_user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        token_header = {"Authorization": f"Bearer {token}"}

    with freeze_time(f"2023-12-28 12:{overtime_minutes}:00"):
        response = await client.post(f"{settings.base_auth_route}/refresh-token", headers=token_header)

        response_json = response.json()
        user_info = response_json["user_info"]

        assert response.status_code == 200
        assert "access_token" in response_json
        assert validate_datetime(response_json["expiration"])

        assert UUID(user_info["id"])
        assert user_info["email"] == normal_user.email
        assert user_info["username"] == normal_user.username
        assert user_info["is_active"] is True
        assert validate_datetime(user_info["created_at"])
        assert validate_datetime(user_info["updated_at"])


@pytest.mark.anyio
async def test_auth_sign_up_should_return_200_OK_POST(client, session, user_factory):
    response = await client.post(
        f"{settings.base_auth_route}/sign-up",
        json={"email": user_factory.email, "password": user_factory.password, "username": user_factory.username},
    )
    response_json = response.json()

    assert response.status_code == 201
    assert UUID(response_json["id"])
    assert response_json["email"] == user_factory.email
    assert response_json["username"] == user_factory.username
    assert response_json["is_active"] is True
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_auth_sign_up_should_return_409_username_already_registered_POST(client, session, normal_user):
    response = await client.post(
        f"{settings.base_auth_route}/sign-up",
        json={"email": "different@email.com", "username": normal_user.username, "password": normal_user.clean_password},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Username already registered"}


@pytest.mark.anyio
async def test_auth_sign_up_should_return_409_email_already_registered_POST(client, session, normal_user):
    response = await client.post(
        f"{settings.base_auth_route}/sign-up",
        json={"email": normal_user.email, "username": "different_username", "password": normal_user.clean_password},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


ic
