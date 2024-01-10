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
        pass

    @classmethod
    async def get_clients_manager(cls, client_tg_id: str):
        pass
