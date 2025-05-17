import pytest


@pytest.mark.anyio
async def test_ping_route_should_return_200_OK_GET(client):
    response = await client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"detail": "Success"}
