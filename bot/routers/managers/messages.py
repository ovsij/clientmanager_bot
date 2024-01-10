from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.dao.chat import ChatDAO

managers_messages_router = Router()


@managers_messages_router.message()
async def get_description(message: Message, state: FSMContext, bot : Bot):
    pass
