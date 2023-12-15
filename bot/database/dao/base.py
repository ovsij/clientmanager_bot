from typing import Any, Dict, Union

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_one(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, db_obj: model, obj_in: Union[model, Dict[str, Any]]):
        async with async_session_maker() as session:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_none=True)
            query = (
                update(cls.model)
                .values(**update_data)
                .where(cls.model.id == db_obj.id)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
