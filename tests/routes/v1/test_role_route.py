from urllib.parse import urlencode

import pytest
from icecream import ic

from tests.helpers import setup_role_data
from tests.helpers import validate_datetime


base_role_route: str = "/v1/role"


# POST - CREATE
@pytest.mark.anyio
async def test_create_normal_roles_should_return_201_POST(client, session, role_factory, admin_user_token, tenant):
    response = await client.post(
        f"{base_role_route}/",
        json={"tenant_id": str(tenant.id), "name": role_factory.name, "description": role_factory.description},
        headers=admin_user_token,
    )
    response_json = response.json()
    assert response.status_code == 201
    assert response_json["name"] == role_factory.name
    assert response_json["description"] == role_factory.description
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_create_normal_role_should_return_422_unprocessable_entity_POST(client, session, admin_user_token):
    response = await client.post(f"{base_role_route}/", headers=admin_user_token)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_normal_role_should_return_409_role_in_this_tenant_already_registered_POST(
    client, session, admin_user_token, role
):
    response = await client.post(
        f"{base_role_route}/",
        json={"tenant_id": str(role.tenant_id), "name": role.name, "description": role.description},
        headers=admin_user_token,
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Role already registered"}


# POST - CREATE
@pytest.mark.anyio
async def test_create_same_roles_with_diferent_should_return_201_POST(client, session, role, admin_user_token, tenant):
    response = await client.post(
        f"{base_role_route}/",
        json={"tenant_id": str(tenant.id), "name": role.name, "description": role.description},
        headers=admin_user_token,
    )
    response_json = response.json()
    assert response.status_code == 201
    assert response_json["name"] == role.name
    assert response_json["description"] == role.description
    assert response_json["tenant_id"] == str(tenant.id)
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


# GET - ALL


@pytest.mark.anyio
async def test_get_all_roles_should_return_200_OK_GET(
    session, client, default_created_search_options, admin_user_token
):
    default_created_search_options["ordering"] = "-name"
    await setup_role_data(session, role_qty=8)
    response = await client.get(
        f"{base_role_route}/?{urlencode(default_created_search_options)}", headers=admin_user_token
    )
    response_json = response.json()
    response_founds = response_json["founds"]

    assert response.status_code == 200
    assert len(response_founds) == 8
    assert response_json["search_options"] == default_created_search_options | {"total_count": 8}
    assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
    assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])


@pytest.mark.anyio
async def test_get_all_roles_with_page_size_should_return_200_OK_GET(session, client, admin_user_token):
    query_find_parameters = {"ordering": "id", "page": 1, "page_size": 5}
    await setup_role_data(session, 5)
    response = await client.get(f"{base_role_route}/?{urlencode(query_find_parameters)}", headers=admin_user_token)
    response_json = response.json()
    response_founds = response_json["founds"]
    assert response.status_code == 200
    assert len(response_founds) == 5
    assert response_json["search_options"] == query_find_parameters | {"total_count": 5}
    assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
    assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])


@pytest.mark.anyio
async def test_get_all_roles_with_pagination_should_return_200_OK_GET(session, client, admin_user_token):
    query_find_parameters = {"ordering": "id", "page": 2, "page_size": 4}
    await setup_role_data(session, 8)
    response = await client.get(f"{base_role_route}/?{urlencode(query_find_parameters)}", headers=admin_user_token)
    response_json = response.json()
    response_founds = response_json["founds"]

    assert response.status_code == 200
    assert len(response_founds) == query_find_parameters["page_size"]
    assert response_json["search_options"] == query_find_parameters | {
        "total_count": query_find_parameters["page_size"]
    }
    assert all([validate_datetime(skill["created_at"]) for skill in response_founds])
    assert all([validate_datetime(skill["updated_at"]) for skill in response_founds])


# DELETE


@pytest.mark.anyio
async def test_delete_role_should_return_204_OK_DELETE(session, client, admin_user_token, role):
    response = await client.delete(f"{base_role_route}/{role.id}", headers=admin_user_token)
    get_roles_response = await client.get(f"{base_role_route}/", headers=admin_user_token)

    assert response.status_code == 204
    assert get_roles_response.status_code == 200
    assert len(get_roles_response.json()["founds"]) == 0


@pytest.mark.anyio
async def test_delete_role_should_return_403_FORBIDDEN_DELETE(
    session, client, normal_user_token, role, admin_user_token
):
    response = await client.delete(f"{base_role_route}/{role.id}", headers=normal_user_token)
    response_json = response.json()
    get_roles_response = await client.get(f"{base_role_route}/", headers=admin_user_token)

    assert response.status_code == 403
    assert response_json == {"detail": "Not enough permissions"}
    assert get_roles_response.status_code == 200
    assert len(get_roles_response.json()["founds"]) == 1


# GET - BY ID


@pytest.mark.anyio
async def test_get_role_by_id_should_return_200_OK_GET(session, client, role, admin_user_token):
    response = await client.get(f"{base_role_route}/{role.id}", headers=admin_user_token)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["name"] == role.name
    assert response_json["description"] == role.description
    assert response_json["tenant_id"] == str(role.tenant_id)
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])


@pytest.mark.anyio
async def test_get_role_by_id_should_return_404_NOT_FOUND_GET(session, client, random_uuid, admin_user_token):
    response = await client.get(f"{base_role_route}/{random_uuid}", headers=admin_user_token)
    assert response.status_code == 404
    assert response.json() == {"detail": f"id not found: {random_uuid}"}


# PUT


@pytest.mark.anyio
async def test_put_role_should_return_200_OK_PUT(session, client, role_factory, role, admin_user_token):
    different_role = {
        "name": role_factory.name,
        "description": role_factory.description,
    }
    ic(different_role)
    response = await client.put(f"{base_role_route}/{role.id}", headers=admin_user_token, json=different_role)
    response_json = response.json()
    assert response.status_code == 200
    assert validate_datetime(response_json["created_at"])
    assert validate_datetime(response_json["updated_at"])
    assert all([response_json[key] == value for key, value in different_role.items()])


@pytest.mark.anyio
async def test_put_other_id_role_should_return_404_NOT_FOUND_PUT(
    session, client, role_factory, role, admin_user_token, random_uuid
):
    different_role = {
        "name": role.name,
        "description": role.description,
    }
    response = await client.put(f"{base_role_route}/{random_uuid}", headers=admin_user_token, json=different_role)
    response_json = response.json()
    assert response.status_code == 404
    assert response_json == {"detail": f"id not found: {random_uuid}"}


@pytest.mark.anyio
async def test_put_same_role_should_return_400_BAD_REQUEST_PUT(session, client, role, admin_user_token):
    different_role = {
        "name": role.name,
        "description": role.description,
    }
    response = await client.put(f"{base_role_route}/{role.id}", headers=admin_user_token, json=different_role)
    response_json = response.json()
    assert response.status_code == 400
    assert response_json == {"detail": "No changes detected"}


@pytest.mark.anyio
async def test_put_role_should_return_403_FORBIDDEN(session, client, role_factory, role, normal_user_token):
    different_role = {
        "name": role_factory.name,
        "description": role_factory.description,
    }
    response = await client.put(f"{base_role_route}/{role.id}", headers=normal_user_token, json=different_role)
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.status_code == 403


ic
