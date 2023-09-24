from datetime import date

from sqlalchemy import and_, update, select
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import CannotUpdateDataToDatabase
from app.orders.models import Orders
from app.performers.orders.models import ExecutorOrders


class ExecutorOrderDAO(BaseDAO):
    model = ExecutorOrders

    @classmethod
    async def find_order_with_pay_method(cls, method_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(cls.model.order_pay_method == method_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update_info_executor_one_in_order(cls, order_id, values):
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

            if "order_num" in values:
                new_profit_query = await ExecutorOrderDAO.find_all(order_num=values["order_num"])
                new_profit = 0
                order_id = values["order_num"]
                if len(new_profit_query) != 0:
                    for i in range(len(new_profit_query)):
                        if new_profit_query[i].order_sum is not None:
                            new_profit += int(new_profit_query[i].order_sum)
                    update_query = (
                        update(Orders)
                        .where(Orders.id == order_id)
                        .values(order_profit=Orders.order_sum - new_profit)
                    )
                    await session.execute(update_query)
                    await session.commit()
                else:
                    update_query = (
                        update(Orders)
                        .where(Orders.id == order_id)
                        .values(order_profit=Orders.order_sum - new_profit)
                    )
                    await session.execute(update_query)
                    await session.commit()

    @classmethod
    async def find_order_id_by_order_num(cls, order_num: int):
        async with async_session_maker() as session:
            query_id = select(Orders).filter_by(order_num=order_num)
            get_order_id = await session.execute(query_id)
            get_order_id_scalar = get_order_id.scalar()
            return get_order_id_scalar.id

    @classmethod
    async def get_all_executors_orders_by_id(cls, order_id: int):
        async with async_session_maker() as session:
            query = select(ExecutorOrders).filter_by(order_num=order_id).options(
                joinedload(ExecutorOrders.executor),
                joinedload(ExecutorOrders.status),
                joinedload(ExecutorOrders.pays),
                joinedload(ExecutorOrders.service)
            )
            results = await session.execute(query)
            if results:
                return results.scalars().all()
            return "Unknown order_exec_data"

    @classmethod
    async def find_executor_order(cls, order_id, executor_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(
                    and_(
                        cls.model.order_num == order_id,
                        cls.model.order_executor == executor_id
                    )
                )
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update_status_executor_order(cls, order_num, order_executors, order_status):
        async with async_session_maker() as session:
            update_query = (
                update(cls.model)
                .where(
                    and_(
                        cls.model.order_num == order_num,
                        cls.model.order_executor == order_executors
                    )
                )
                .values(order_status=order_status)
            )

            await session.execute(update_query)
            if order_status == 5:
                update_query = (
                    update(cls.model)
                    .where(
                        and_(
                            cls.model.order_num == order_num,
                            cls.model.order_executor == order_executors
                        )
                    )
                    .values(order_date_close=date.today())
                )
            result = await session.execute(update_query)
            await session.commit()
            return result
