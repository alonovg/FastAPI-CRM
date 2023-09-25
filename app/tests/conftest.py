import asyncio
from datetime import datetime
import json

from unittest import mock
import pytest
from sqlalchemy import insert
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.clients.models import Clients
from app.orders.models import Orders
from app.paysmethods.models import PaysMethods
from app.performers.executors.models import Executors
from app.performers.orders.models import ExecutorOrders
from app.performers.services.models import Services
from app.statuses.models import Statuses
from app.users.models import Users
from app.main import app as fastapi_app


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_files/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    clients = open_mock_json("clients")
    executors = open_mock_json("executors")
    pays_methods = open_mock_json("pays_methods")
    services = open_mock_json("services")
    statuses = open_mock_json("statuses")
    users = open_mock_json("users")
    orders = open_mock_json("orders")
    executor_orders = open_mock_json("executor_orders")

    for order in orders:
        order["order_date_create"] = datetime.strptime(order["order_date_create"], "%Y-%m-%d")

    for executor_order in executor_orders:
        executor_order["order_date_create"] = datetime.strptime(executor_order["order_date_create"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_clients = insert(Clients).values(clients)
        add_executors = insert(Executors).values(executors)
        add_pays_methods = insert(PaysMethods).values(pays_methods)
        add_services = insert(Services).values(services)
        add_statuses = insert(Statuses).values(statuses)
        add_users = insert(Users).values(users)
        add_orders = insert(Orders).values(orders)
        add_executor_orders = insert(ExecutorOrders).values(executor_orders)

        await session.execute(add_clients)
        await session.execute(add_executors)
        await session.execute(add_pays_methods)
        await session.execute(add_services)
        await session.execute(add_statuses)
        await session.execute(add_users)
        await session.execute(add_orders)
        await session.execute(add_executor_orders)

        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
