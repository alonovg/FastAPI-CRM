from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import CannotFindStatus
from app.statuses.dao import StatusDAO
from app.statuses.schemas import SStatus


router = APIRouter(
    prefix="/statuses",
    tags=["Статусы заявок"]
)


@router.post("/add-status")
async def add_status(client_data: SStatus):
    """Добавление статуса заявки"""
    return await StatusDAO.add(name=client_data.name)


@router.get("/get-statuses")
@cache(expire=60)
async def get_statuses():
    """Получение списка статусов заявок - Кэшируется в Redis на 60 секунд."""
    return await StatusDAO.find_all()


@router.delete("/delete-status/{id}")
async def delete_status(status_id: int):
    """Удаление статуса заявки"""
    find_status = await StatusDAO.find_one_or_none(id=status_id)
    if not find_status:
        raise CannotFindStatus
    await StatusDAO.delete(id=status_id)
    return {"message": "Статус успешно удален",
            "status_id": status_id,
            "status_name": find_status.name}
