from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import async_session_maker
from app.orders.models import Orders
from app.performers.orders.dao import ExecutorOrderDAO
from app.users.dependencies import get_current_user


async def check_authentication(request: Request = Depends()):
    if not get_current_user:
        return RedirectResponse("login.html")
    return request


async def get_orders_info_async_func():
    async with async_session_maker() as session:
        query = select(Orders).options(joinedload(Orders.user),
                                       joinedload(Orders.client),
                                       joinedload(Orders.pays),
                                       joinedload(Orders.status))
        results = await session.execute(query)
        if results:
            return results.scalars().all()
        return "Unknown order_data"


async def func_for_calc_gets_spends_2func(dict1, inner_func_1, inner_func_2) -> list:
    results_1, results_2 = [], []
    for result in dict1:
        res_first = await inner_func_1(result["id"])
        results_1.append(res_first)
        res_second = await inner_func_2(result["id"])
        results_2.append(res_second)
    return list(zip(dict1, results_1, results_2))


async def func_for_calc_gets_spends_1func(dict1, inner_func_1) -> list:
    results_1 = []
    for result in dict1:
        res_first = await inner_func_1(result["id"])
        results_1.append(res_first)
    return list(zip(dict1, results_1))


async def get_count_executor_by_id(order_id: int):
    """Получение количества исполнителей в заказе по id заказа"""
    result = await ExecutorOrderDAO.get_all_executors_orders_by_id(order_id)
    return len(result)
