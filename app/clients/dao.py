from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.clients.models import Clients
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.orders.models import Orders


class ClientDAO(BaseDAO):
    model = Clients

    @classmethod
    async def get_all_order_profit_by_client(cls, client_id: int):
        async with async_session_maker() as session:
            query = select(Orders.order_profit).filter_by(order_client=client_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_all_order_for_client(cls, client_id: int):
        async with async_session_maker() as session:
            query = select(Orders).filter_by(order_client=client_id).options(joinedload(Orders.pays),
                                                                             joinedload(Orders.status))
            result = await session.execute(query)
            return result.scalars().all()

