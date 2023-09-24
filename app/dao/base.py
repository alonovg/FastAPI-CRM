from sqlalchemy import select, insert, delete, update

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_spend_sum(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.order_sum).filter_by(**filter_by)
            results = await session.execute(query)
            results_scalar = results.scalars().all()
            sum_res = 0
            for result in results_scalar:
                if result:
                    sum_res += result
            return sum_res

    @classmethod
    async def update(cls, data_id, **values):
        async with async_session_maker() as session:
            query = (update(cls.model)
                     .where(cls.model.id == data_id)
                     .values(**values)
                     )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data).returning(cls.model.id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
