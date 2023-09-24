from datetime import date

from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.exceptions import CannotUpdateDataToDatabase
from app.orders.models import Orders
from app.database import async_session_maker
from app.performers.orders.dao import ExecutorOrderDAO


class OrderDAO(BaseDAO):
    model = Orders

    @classmethod
    async def get_all_data_order_by_id(cls, order_num: int):
        async with async_session_maker() as session:
            query = select(Orders).filter_by(order_num=order_num).options(
                joinedload(Orders.user),
                joinedload(Orders.client),
                joinedload(Orders.pays),
                joinedload(Orders.status),
            )
            results = await session.execute(query)
            if results:
                return results.scalars().all()
            return "Unknown order_data"

    @classmethod
    async def get_last_order_num(cls):
        """
        Function is get last order number by max id.
        :return: Last number of order type: Integer.
        """
        async with async_session_maker() as session:
            query = func.max(cls.model.id)
            last_id = await session.execute(query)
            last_id_scalar = last_id.scalar()
            query_second = select(cls.model).filter_by(id=last_id_scalar)
            last_order = await session.execute(query_second)
            last_order_data = last_order.scalar()
            if not last_order_data:
                return 0
            return last_order_data.order_num

    @classmethod
    async def update_order_info(cls, order_id, values):
        async with async_session_maker() as session:
            update_query = (
                update(cls.model)
                .where(cls.model.id == order_id)
                .values(**values)
            )
            result_update_main_info = await session.execute(update_query)

            if not result_update_main_info:
                raise CannotUpdateDataToDatabase
            await session.commit()

            if "order_status" in values and values["order_status"] in [3, 4, 5]:
                new_status = values["order_status"]
                update_query = (
                    update(cls.model)
                    .where(cls.model.id == order_id)
                    .values(order_status=int(new_status),
                            order_date_close=date.today())
                )
                await session.execute(update_query)
                await session.commit()
            elif "order_status" in values and values["order_status"] not in [3, 4, 5]:
                new_status = values["order_status"]
                update_query = (
                    update(cls.model)
                    .where(cls.model.id == order_id)
                    .values(order_status=int(new_status),
                            order_date_close=None)
                )
                await session.execute(update_query)
                await session.commit()

    @classmethod
    async def set_new_profit(cls, order_id):
        async with async_session_maker() as session:
            new_profit_query = await ExecutorOrderDAO.find_all(order_num=order_id)
            new_profit = 0
            if len(new_profit_query) != 0:
                for i in range(len(new_profit_query)):
                    if new_profit_query[i].order_sum is not None:
                        new_profit += int(new_profit_query[i].order_sum)
                update_query = (
                    update(cls.model)
                    .where(cls.model.id == order_id)
                    .values(order_profit=cls.model.order_sum - new_profit)
                )
                await session.execute(update_query)
                await session.commit()
            else:
                update_query = (
                    update(cls.model)
                    .where(cls.model.id == order_id)
                    .values(order_profit=cls.model.order_sum - new_profit)
                )
                await session.execute(update_query)
                await session.commit()
