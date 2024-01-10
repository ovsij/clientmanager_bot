from sqlalchemy import or_, select

from bot.database.dao.base import BaseDAO
from bot.database.dao.users import UserDAO
from bot.database.database import async_session_maker
from bot.database.models.chat import Chat
from bot.database.models.users import User


class ChatDAO(BaseDAO):
    model = Chat

    @classmethod
    async def add_one(cls, tg_id: str):
        pass

    @classmethod
    async def get_not_archived(cls, manager_tg_id: str):
        pass

    @classmethod
    async def update(cls, client_id, manager_tg_id: str, is_open: bool):
        pass

    @classmethod
    async def get_users_in_open(cls):
        pass

    @classmethod
    async def get_receiver(cls, tg_id: str):
        pass
