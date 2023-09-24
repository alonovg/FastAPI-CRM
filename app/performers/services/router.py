from typing import Annotated

from fastapi import APIRouter, Form
from fastapi_cache.decorator import cache

from app.exceptions import CannotFindService, ServiceAlreadyExist
from app.performers.orders.dao import ExecutorOrderDAO
from app.performers.services.dao import ServiceDAO


router = APIRouter(
    prefix="/services",
    tags=["Услуги"]
)


@router.post("/del_service")
async def del_service(service_id: Annotated[int, Form()]):
    """Удаляет услугу"""
    find_service = await ServiceDAO.find_one_or_none(id=service_id)
    if not find_service:
        raise CannotFindService
    await ServiceDAO.delete(id=service_id)
    return {"message": "Услуга успешно удалена",
            "service_id": service_id,
            "service_name": find_service.name}


@router.post("/add_service")
async def add_service(
        name: Annotated[str, Form()]
):
    """Добавляет услугу"""
    find_service = await ServiceDAO.find_one_or_none(name=name)
    if find_service:
        raise ServiceAlreadyExist
    result = await ServiceDAO.add(name=name)
    return {"message": "Услуга успешно добавлена",
            "service_id": result.id}


@router.get("/get-all")
@cache(expire=60)
async def get_services():
    """Получает список всех услуг - Кэшируется в Redis на 60 секунд."""
    return await ServiceDAO.find_all()


@router.get("/get/spend/sum")
async def get_spend_sum_by_pays_service(order_service_id: int):
    """Получает сумму полученных средств по id услуги"""
    find_service = await ServiceDAO.find_one_or_none(id=order_service_id)
    if not find_service:
        raise CannotFindService
    result_sum = await ExecutorOrderDAO.get_spend_sum(order_service=order_service_id)
    return {"result_sum": result_sum}
