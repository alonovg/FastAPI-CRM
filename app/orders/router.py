from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from app.clients.dao import ClientDAO
from app.exceptions import (CannotFindClient, CannotFindPayMethod, CannotFindStatus,
                            CannotFindOrder, CannotUpdateDataToDatabase)
from app.orders.dao import OrderDAO
from app.pages.dependencies import get_count_executor_by_id
from app.paysmethods.dao import PaysMethodDAO
from app.performers.orders.dao import ExecutorOrderDAO
from app.statuses.dao import StatusDAO
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)


@router.post("/update/order_info")
async def update_order_info(
        order_id: Annotated[int, Form()],
        order_name: Annotated[str, Form()],
        order_status: Annotated[int, Form()],
        order_get_pay: Annotated[bool, Form()],
        order_sum: Optional[Annotated[float, Form()]] = Form(None),
        order_pay_method: Optional[Annotated[int, Form()]] = Form(None),

):
    """
    Обновление информации о заказе
    :param order_id: id заказа
    :param order_name: Имя заказа
    :param order_status: id статуса заказа
    :param order_get_pay: boolean оплаты заказа
    :param order_sum: optional, сумма заказа
    :param order_pay_method: optional, id метода оплаты заказа
    :return: json
    """
    find_order = await OrderDAO.find_one_or_none(id=order_id)
    order_info_new_data = {}
    if not find_order:
        raise CannotFindOrder
    if order_name != find_order.order_name:
        order_info_new_data["order_name"] = order_name
    if order_status != find_order.order_status:
        find_status = await StatusDAO.find_one_or_none(id=order_status)
        if not find_status:
            raise CannotFindStatus
        order_info_new_data["order_status"] = order_status
    if order_get_pay != find_order.order_get_pay:
        order_info_new_data["order_get_pay"] = order_get_pay
    if (order_sum != 0) and (order_sum != find_order.order_sum):
        order_info_new_data["order_sum"] = order_sum
    if order_pay_method and order_pay_method != find_order.order_pay_method:
        find_pay_method = await PaysMethodDAO.find_one_or_none(id=order_pay_method)
        if not find_pay_method:
            raise CannotFindPayMethod
        order_info_new_data["order_pay_method"] = order_pay_method
    if order_info_new_data:
        await OrderDAO.update_order_info(order_id=int(order_id), values=order_info_new_data)
        await OrderDAO.set_new_profit(order_id=int(order_id))
        return JSONResponse(content={"message": "Данные успешно обновлены", "status": 200}, status_code=200)
    raise CannotUpdateDataToDatabase


@router.post("/add/new_order")
async def add_order(
        order_name: Annotated[str, Form()],
        order_client: Annotated[int, Form()],
        order_get_pay: Annotated[bool, Form()],
        order_status: Annotated[int, Form()],
        order_pay_method: Optional[Annotated[int, Form()]] = Form(None),
        order_sum: Optional[Annotated[float, Form()]] = Form(None),
        user: Users = Depends(get_current_user)
):
    """
    Создает новый заказ
    :param order_name: Имя заказа
    :param order_client: id клиента
    :param order_get_pay: boolean оплаты заказа
    :param order_status: id статуса заказа
    :param order_pay_method: optional, id метода оплаты заказа
    :param order_sum: optional, сумма заказа
    :param user: id пользователя
    :return: json
    """
    find_client = await ClientDAO.find_one_or_none(id=order_client)
    if not find_client:
        raise CannotFindClient
    if order_pay_method:
        find_pay_method = await PaysMethodDAO.find_one_or_none(id=order_pay_method)
        if not find_pay_method:
            raise CannotFindPayMethod
    find_order_status = await StatusDAO.find_one_or_none(id=order_status)
    if not find_order_status:
        raise CannotFindStatus
    if order_status not in [3, 4, 5]:
        order_date_close = None
    else:
        order_date_close = date.today()
    last_order_number = await OrderDAO.get_last_order_num()
    order_creator = user.id
    await OrderDAO.add(
        order_num=last_order_number + 1,
        order_creator=order_creator,
        order_name=order_name,
        order_date_create=date.today(),
        order_date_close=order_date_close,
        order_client=order_client,
        order_get_pay=order_get_pay,
        order_pay_method=order_pay_method,
        order_sum=order_sum,
        order_status=order_status
    )
    content = {
        "message": "Заказ успешно создан",
        "order_num": last_order_number + 1,
        "order_name": order_name,
        "order_client": find_client.username,
        "client_id": order_client,
    }
    return JSONResponse(content=content, status_code=201)


@router.post("/del_order")
async def del_order(order_id: Annotated[int, Form()]):
    """
    Удаляет заказ и всех исполниетелй из него
    :param order_id: id заказа
    :param order_num: Номер заказа
    :return: json
    """
    find_order = await OrderDAO.find_one_or_none(id=order_id)
    if not find_order:
        raise CannotFindOrder
    find_count_executor = await get_count_executor_by_id(order_id)
    for _ in range(find_count_executor):
        await ExecutorOrderDAO.delete(order_num=order_id)
    await OrderDAO.delete(id=order_id)
    context = {
        "message": "Заказ успешно удален",
        "order_id": order_id,
        "exercutor_count": find_count_executor,
    }
    return JSONResponse(content=context, status_code=201)


@router.get("/get-all")
@cache(expire=60)
async def get_orders():
    """Получение всех заказов - Кэшируется в Redis на 60 секунд."""
    return await OrderDAO.find_all()


@router.get("/get-order/{order_num}")
async def get_order_by_num(order_num: int):
    """Получение информации о заказе по номеру"""
    find_order = await OrderDAO.find_one_or_none(order_num=order_num)
    if not find_order:
        raise CannotFindOrder
    return await OrderDAO.get_all_data_order_by_id(order_num=order_num)
