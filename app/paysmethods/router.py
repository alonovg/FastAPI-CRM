from typing import Annotated

from fastapi import APIRouter, Form
from fastapi_cache.decorator import cache

from app.exceptions import CannotFindPayMethod, CannotDelPayMethod
from app.orders.dao import OrderDAO
from app.paysmethods.dao import PaysMethodDAO
from app.paysmethods.schemas import SPayMethod
from app.performers.orders.dao import ExecutorOrderDAO


router = APIRouter(
    prefix="/pays-methods",
    tags=["Платежные средства"]
)


@router.post("/del_pay_method", status_code=201)
async def del_pay_method(method_id: Annotated[int, Form()]):
    """Удаление платежного средства"""
    find_pay_method = await PaysMethodDAO.find_one_or_none(id=method_id)
    if not find_pay_method:
        raise CannotFindPayMethod
    find_order_with_pay_method = await ExecutorOrderDAO.find_order_with_pay_method(method_id)
    if find_order_with_pay_method:
        raise CannotDelPayMethod
    await PaysMethodDAO.delete(id=method_id)
    return {"message": "Успешно удалено",
            "PayMethodId": find_pay_method.id,
            "PayMethodName": find_pay_method.name}


@router.post("/add_pay_method", status_code=201)
async def add_pay_method(
        name: Annotated[str, Form()],
):
    """Добавление платежного средства через форму на сайте"""
    result = await PaysMethodDAO.add(name=name)
    return {"message": "Платежное средство успешно добавлено",
            "id": result.id}


@router.post("/add")
async def add_pay_method(pay_data: SPayMethod):
    """Добавление платежного средства через POST - Json"""
    return await PaysMethodDAO.add(name=pay_data.name)


@router.get("")
@cache(expire=60)
async def get_pays_methods():
    """Получение списка платежных средств - Кэшируется в Redis на 60 секунд."""
    return await PaysMethodDAO.find_all()


@router.get("/get/spend/sum")
async def get_spend_sum_by_pays(pay_method_id: int):
    """Получение суммы по id платежного средства"""
    find_pay_method = await PaysMethodDAO.find_one_or_none(id=pay_method_id)
    if not find_pay_method:
        raise CannotFindPayMethod
    result_sum = await ExecutorOrderDAO.get_spend_sum(order_pay_method=pay_method_id)
    return {"result_sum": result_sum}


@router.get("/get/sum")
async def get_sum_by_pays(pay_method_id: int):
    """Получение суммы оплат по id платежного средства"""
    find_pay_method = await PaysMethodDAO.find_one_or_none(id=pay_method_id)
    if not find_pay_method:
        raise CannotFindPayMethod
    result_sum = await OrderDAO.get_spend_sum(order_pay_method=pay_method_id)
    return {"result_sum": result_sum}
