from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("username, status_code", [
    ("test_client", 201),
])
async def test_add_client(username, status_code, async_client: AsyncClient):
    response = await async_client.post("/clients/add_client", json={"username": username})
    assert response.status_code == status_code


async def test_get_clients(async_client: AsyncClient):
    response = await async_client.get("/clients/get_all_clients")
    assert response.status_code == 200


