from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("name, password, status_code", [
    ("kotopes", "1234", 201),
    ("kotopes", "kot0pes", 409),
])
async def test_register_user(name, password, status_code, async_client: AsyncClient):
    response = await async_client.post("/auth/register", json={"name": name, "password": password})
    assert response.status_code == status_code


@pytest.mark.parametrize("name, password, status_code", [
    ("test", "test", 200),
    ("WrongPerson", "WrongPerson", 401),
])
async def test_login_user(name, password, status_code, async_client: AsyncClient):
    response = await async_client.post("/auth/login", json={"name": name, "password": password})
    assert response.status_code == status_code


async def test_logout_user(async_client: AsyncClient):
    response = await async_client.get("/auth/logout")
    assert response.status_code == 200


async def test_read_users_me(async_client: AsyncClient):
    response = await async_client.get("/auth/me")
    assert response.status_code == 401
