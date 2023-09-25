from typing import Annotated

from fastapi import APIRouter, Form
from fastapi_cache.decorator import cache

from app.clients.dao import ClientDAO
from app.clients.schemas import SClientDelete, SClientNew
from app.exceptions import UserAlreadyExistsException, CannotFindClient
from app.orders.dao import OrderDAO


router = APIRouter(
    prefix="/clients",
    tags=["Клиенты"]
)


@router.post("/add_client", status_code=201)
# async def add_client(username: Annotated[str, Form()]):
async def add_client(client_data: SClientNew):
    """Добавляет клиента в базу данных"""
    find_client = await ClientDAO.find_one_or_none(username=client_data.username)
    if find_client:
        raise UserAlreadyExistsException
    result = await ClientDAO.add(username=client_data.username)
    return {"message": "Client created successfully",
            "id": result.id}


@router.post("/del_client", status_code=200)
# async def del_client(client_id: Annotated[int, Form()]):
async def del_client(client: SClientDelete):
    """Удаляет клиента из базы данных"""
    find_client = await ClientDAO.find_one_or_none(id=client.id)
    if not find_client:
        raise CannotFindClient
    await ClientDAO.delete(id=client.id)
    return {"message": "Client deleted successfully"}


@router.post("/update_client", status_code=200)  # patch
async def update_client(client_id: Annotated[int, Form()], new_username: Annotated[str, Form()]):
    """Обновляет клиента из базы данных"""
    find_client = await ClientDAO.find_one_or_none(id=client_id)
    if not find_client:
        raise CannotFindClient
    await ClientDAO.update(data_id=client_id, username=new_username)
    return {"message": "Client updated successfully"}


@router.get("/get_all_clients")
# @cache(expire=60)
async def get_clients():
    """Получает список всех клиентов - Кэшируется в Redis на 60 секунд."""
    return await ClientDAO.find_all()


@router.get("/get_client_by_id")
async def get_one_client_by_id(client_id: int):
    """Получает клиента по его id"""
    return await ClientDAO.find_one_or_none(id=client_id)


@router.get("/ge_-client_order")
async def get_client_order(client_id: int):
    """Получает список всех заказов для клиента"""
    return await ClientDAO.get_all_order_for_client(client_id=client_id)


@router.get("/get_profit_order")
async def get_profit_from_all_order(client_id: int):
    """Получает принесенную прибыль от всех заказов для клиента"""
    find_client = await ClientDAO.find_one_or_none(id=client_id)
    if not find_client:
        raise CannotFindClient
    results = await ClientDAO.get_all_order_profit_by_client(client_id=client_id)
    profit = 0
    for result in results:
        if result:
            profit += result
    return {"profit": profit}


@router.get("/get/sum/order")
async def get_sum_from_all_order(client_id: int):
    """Получает сумму прибыль от всех заказов для клиента"""
    find_client = await ClientDAO.find_one_or_none(id=client_id)
    if not find_client:
        raise CannotFindClient
    result_sum = await OrderDAO.get_spend_sum(order_client=client_id)
    return {"result_sum": result_sum}
