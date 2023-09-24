from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.exceptions import (CannotFindOrder, CannotFindExecutor, CannotFindStatus, CannotFindPayMethod,
                            CannotFindService, CannotUpdateDataToDatabase, CannotFindExecutorInOrder)
from app.orders.dao import OrderDAO
from app.paysmethods.dao import PaysMethodDAO
from app.performers.executors.dao import ExecutorDAO
from app.performers.orders.dao import ExecutorOrderDAO
from app.performers.services.dao import ServiceDAO
from app.statuses.dao import StatusDAO


router = APIRouter(
    prefix="/performers",
    tags=["Заказы исполнителей"]
)


@router.post("/del/executor-from-order/", status_code=201)
async def del_executor_from_order_by_id(
        executor_orders_id: Annotated[int, Form()],
        order_page_num: Annotated[int, Form()]
):
    """Удаляет исполнителя из заказа
    executor_orders_id - id заказа из таблицы executor_orders
    order_page_num - номер заказа из таблицы orders
    """
    find_executor_order = await ExecutorOrderDAO.find_one_or_none(id=executor_orders_id)
    if not find_executor_order:
        raise CannotFindExecutorInOrder
    find_executor = await ExecutorDAO.find_one_or_none(id=find_executor_order.order_executor)
    await ExecutorOrderDAO.delete(id=executor_orders_id)
    await OrderDAO.set_new_profit(order_id=int(find_executor_order.order_num))
    return {"message": "Успешно удален исполнитель",
            "executor_name": find_executor.name,
            "order_id": find_executor_order.order_num,
            "order_num": order_page_num}


@router.post("/update/executor-info", status_code=200)
async def update_executor_info_for_order(
        order_name: Annotated[str, Form()],
        order_id: Annotated[int, Form()],
        order_send_pay: Annotated[bool, Form()],
        order_pay_method: Optional[Annotated[int, Form()]] = Form(None),
        order_status: Optional[Annotated[int, Form()]] = Form(None),
        order_sum: Optional[Annotated[float, Form()]] = Form(None),
):
    """
    Обновляет информацию о исполнителе в заказе
    :param order_name: Описание заявки
    :param order_id: id заказа из таблицы executor_orders
    :param order_send_pay: bool
    :param order_pay_method: optional, id платежной системы из таблицы pays_methods
    :param order_status: optional, id статуса заказа из таблицы statuses
    :param order_sum: optional, сумма оплаты исполнителю
    :return: json
    """
    find_executor_order = await ExecutorOrderDAO.find_one_or_none(id=order_id)
    if not find_executor_order:
        raise CannotFindExecutorInOrder
    if order_pay_method:
        find_pay_method = await PaysMethodDAO.find_one_or_none(id=order_pay_method)
        if not find_pay_method:
            raise CannotFindPayMethod
    if order_status:
        find_order_status = await StatusDAO.find_one_or_none(id=order_status)
        if not find_order_status:
            raise CannotFindStatus
    executor_new_info = {}
    executor_new_info["order_num"] = find_executor_order.order_num
    if order_name != find_executor_order.order_name:
        executor_new_info["order_name"] = order_name
    if order_pay_method and order_pay_method != find_executor_order.order_pay_method:
        executor_new_info["order_pay_method"] = order_pay_method
    if order_send_pay != find_executor_order.order_send_pay:
        executor_new_info["order_send_pay"] = order_send_pay
    if order_status and order_status != find_executor_order.order_status:
        executor_new_info["order_status"] = order_status
    if order_sum != 0 and order_sum != find_executor_order.order_sum:
        executor_new_info["order_sum"] = order_sum
    if executor_new_info:
        await ExecutorOrderDAO.update_info_executor_one_in_order(order_id=order_id, values=executor_new_info)
        return JSONResponse(content={"message": "Данные успешно обновлены", "status": 200}, status_code=200)
    raise CannotUpdateDataToDatabase


@router.post("/new_exec")
async def add_order_from_site_executor(
        order_num: Annotated[int, Form()],
        order_executor: Annotated[int, Form()],
        order_status: Annotated[int, Form()],
        order_send_pay: Annotated[bool, Form()],
        order_service: Annotated[int, Form()],
        order_page_num: Annotated[int, Form()],
        order_name: Optional[Annotated[str, Form()]] = Form(None),
        order_pay_method: Optional[Annotated[int, Form()]] = Form(None),
        order_sum: Optional[Annotated[float, Form()]] = Form(None)

):
    """
    Добавление исполнителя в заказ
    :param order_num: id заявки из таблицы orders
    :param order_executor: id исполнителя из таблицы executors
    :param order_status: id статуса заказа из таблицы statuses
    :param order_send_pay: bool
    :param order_service: id сервиса из таблицы services
    :param order_page_num: номер заказа из таблицы orders (order_num)
    :param order_name: optional, описание заявки
    :param order_pay_method: optional, id платежной системы из таблицы
    :param order_sum: optional, сумма оплаты исполнителю
    :return: json
    """
    find_order_num = await OrderDAO.find_one_or_none(id=order_num)
    if not find_order_num:
        raise CannotFindOrder
    find_order_executor = await ExecutorDAO.find_one_or_none(id=order_executor)
    if not find_order_executor:
        raise CannotFindExecutor
    find_order_status = await StatusDAO.find_one_or_none(id=order_status)
    if not find_order_status:
        raise CannotFindStatus
    if order_pay_method:
        find_pay_method = await PaysMethodDAO.find_one_or_none(id=order_pay_method)
        if not find_pay_method:
            raise CannotFindPayMethod
    find_order_service = await ServiceDAO.find_one_or_none(id=order_service)
    if not find_order_service:
        raise CannotFindService
    if order_status not in [3, 4, 5]:
        order_date_close = None
    else:
        order_date_close = date.today()
    order_executor = await ExecutorOrderDAO.add(
        order_name=order_name,
        order_num=order_num,
        order_executor=order_executor,
        order_status=order_status,
        order_send_pay=order_send_pay,
        order_pay_method=order_pay_method,
        order_sum=order_sum,
        order_service=order_service,
        order_date_create=date.today(),
        order_date_close=order_date_close
    )
    await OrderDAO.set_new_profit(order_id=int(order_num))
    return JSONResponse(content={
        "message": f"Исполнитель {find_order_executor.name} успешно добавлен для заявки #{order_page_num}",
        "order_num": order_num,
        "executor_orders_id": order_executor.id,
        "status": 200}, status_code=200)


@router.get("/test/111/{order_num}")
async def get_order_exc_by_num(order_num: int):
    """Получение списка исполнителей в заказе по номеру заказа"""
    find_order = await OrderDAO.find_one_or_none(order_num=order_num)
    if not find_order:
        raise CannotFindOrder
    find_order_id = await ExecutorOrderDAO.find_order_id_by_order_num(order_num=order_num)
    return await ExecutorOrderDAO.get_all_executors_orders_by_id(order_id=find_order_id)


@router.get("")
@cache(expire=60)
async def get_executors_orders():
    """Получение списка заказов исполнителей - Кэшируется в Redis на 60 секунд."""
    return await ExecutorOrderDAO.find_all()


@router.patch("/update-status")
async def update_order_executors_status(
    order_num: int,
    order_executor: int,
    order_status: int
):
    """
    Обновлять статус заказа исполнителя в основном заказе
    :param order_num: id заявки
    :param order_executor: id исполнителя из таблицы executors
    :param order_status: id статуса заказа из таблицы statuses
    :return: json
    """
    find_order_num = await OrderDAO.find_one_or_none(order_num=order_num)
    if not find_order_num:
        raise CannotFindOrder
    find_order_executor = await ExecutorDAO.find_one_or_none(id=order_executor)
    if not find_order_executor:
        raise CannotFindExecutor
    find_order_status = await StatusDAO.find_one_or_none(id=order_status)
    if not find_order_status:
        raise CannotFindStatus
    find_order = await ExecutorOrderDAO.find_executor_order(order_id=order_num, executor_id=order_executor)
    if not find_order:
        raise CannotFindExecutorInOrder
    await ExecutorOrderDAO.update_status_executor_order(order_num, order_executor, order_status)
    return JSONResponse(content={"message": "Данные успешно обновлены", "status": 200}, status_code=200)
