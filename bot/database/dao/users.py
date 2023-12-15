import asyncio

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.dao.base import BaseDAO
from bot.database.database import async_session_maker
from bot.database.models.users import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_free_manager(cls):
        """
        Get a manager with fewer clients
        """
        async with async_session_maker() as session:
            subquery = (
                select(User.manager_id, func.count(User.id).label("client_count"))
                .where(User.is_manager == True)
                .group_by(User.manager_id)
                .alias("subquery")
            )

            query = (
                select(User)
                .join(subquery, subquery.c.manager_id == User.id, isouter=True)
                .order_by(func.coalesce(subquery.c.client_count, 0))
            )

            manager = (await session.execute(query)).scalar()
            if manager:
                return manager
            return None

    @classmethod
    async def get_clients_manager(cls, client_tg_id: str):
        client = await super().get_one_or_none(tg_id=client_tg_id)
        manager = await super().get_by_id(model_id=client.manager_id)
        return client, manager
