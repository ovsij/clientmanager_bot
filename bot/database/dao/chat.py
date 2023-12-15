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
        client, manager = await UserDAO.get_clients_manager(client_tg_id=tg_id)
        await super().add_one(client_id=client.id, manager_id=manager.id)

    @classmethod
    async def get_not_archived(cls, manager_tg_id: str):
        manager = await UserDAO.get_one_or_none(tg_id=manager_tg_id)
        async with async_session_maker() as session:
            query = (
                select(Chat.client_id)
                .where(Chat.is_archived.is_(False))
                .where(Chat.manager_id == manager.id)
            )
            result = await session.execute(query)
            clients_with_active_chat = [client_id for (client_id,) in result.all()]
            return clients_with_active_chat

    @classmethod
    async def update(cls, client_id, manager_tg_id: str, is_open: bool):
        manager = await UserDAO.get_one_or_none(tg_id=manager_tg_id)
        client = await UserDAO.get_by_id(model_id=client_id)
        chat = await super().get_one_or_none(client_id=client.id, manager_id=manager.id)
        await super().update(chat, {"is_open": is_open})

    @classmethod
    async def get_users_in_open(cls):
        async with async_session_maker() as session:
            subquery_client = (
                select(Chat.client_id)
                .where(Chat.is_open.is_(True))
                .distinct()
                .subquery()
            )

            subquery_manager = (
                select(Chat.manager_id)
                .where(Chat.is_open.is_(True))
                .distinct()
                .subquery()
            )

            query = select(User.tg_id).where(
                or_(
                    User.id.in_(select(subquery_client)),
                    User.id.in_(select(subquery_manager)),
                )
            )

            result = await session.execute(query)
            users_with_open_chats = result.scalars().all()

            return users_with_open_chats

    @classmethod
    async def get_receiver(cls, tg_id: str):
        async with async_session_maker() as session:
            user = await session.execute(select(User).where(User.tg_id == tg_id))
            user = user.scalar_one_or_none()

            if not user:
                return None

            is_manager = user.is_manager

            if is_manager:
                chat = (
                    select(Chat.client_id)
                    .where(Chat.manager_id == user.id)
                    .where(Chat.is_open.is_(True))
                    .distinct()
                )
                partner_id = await session.execute(chat)
                partner_id = partner_id.scalar_one_or_none()
            else:
                chat = (
                    select(Chat.manager_id)
                    .where(Chat.client_id == user.id)
                    .where(Chat.is_open.is_(True))
                    .distinct()
                )
                partner_id = await session.execute(chat)
                partner_id = partner_id.scalar_one_or_none()

            if partner_id:
                partner = await session.execute(
                    select(User).where(User.id == partner_id)
                )
                partner = partner.scalar_one()
                return partner.tg_id

            return None
