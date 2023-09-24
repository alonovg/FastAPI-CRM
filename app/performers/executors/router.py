from typing import Annotated

from fastapi import APIRouter, Form
from fastapi_cache.decorator import cache

from app.exceptions import CannotFindExecutor, ExecutorExistInOrders, ExecutorAlreadyExist
from app.performers.executors.dao import ExecutorDAO
from app.performers.orders.dao import ExecutorOrderDAO


router = APIRouter(
    prefix="/executors",
    tags=["Исполнители"]
)


@router.post("/del_executor")
async def del_executor(executor_id: Annotated[int, Form()]):
    """Удаление исполнителя"""
    find_executor = await ExecutorDAO.find_one_or_none(id=executor_id)
    if not find_executor:
        raise CannotFindExecutor
    existing_executor_orders = await ExecutorOrderDAO.find_one_or_none(order_executor=executor_id)
    if existing_executor_orders:
        raise ExecutorExistInOrders
    await ExecutorDAO.delete(id=executor_id)
    return {"message": "Успешно удален",
            "executor_id": executor_id,
            "name": find_executor.name}


@router.post("/add_executor")
async def add_executor(
        name: Annotated[str, Form()]
):
    """Добавление исполнителя"""
    existing_executor = await ExecutorDAO.find_one_or_none(name=name)
    if existing_executor:
        raise ExecutorAlreadyExist
    result = await ExecutorDAO.add(name=name)
    return {"message": "Успешно добавлен",
            "executor_id": result.id,
            "name": name}


@router.get("/get-all-executors")
@cache(expire=60)
async def get_executors():
    """Получение списка исполнителей - Кэшируется в Redis на 60 секунд."""
    return await ExecutorDAO.find_all()


@router.get("/get-spend-sum")
async def get_spend_sum_by_pays_executor(order_executor_id: int):
    find_executor = await ExecutorDAO.find_one_or_none(id=order_executor_id)
    if not find_executor:
        raise CannotFindExecutor
    result_sum = await ExecutorOrderDAO.get_spend_sum(order_executor=order_executor_id)
    return {"result_sum": result_sum}
