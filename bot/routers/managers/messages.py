from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.dao.chat import ChatDAO

managers_messages_router = Router()


"""@managers_messages_router.message()
async def get_description(message: Message, state: FSMContext, bot : Bot):
    users_in_open = await ChatDAO.get_users_in_open()
    print(users_in_open)
    if str(message.from_user.id) in users_in_open:
        receiver = await ChatDAO.get_receiver(tg_id=str(message.from_user.id))
        print(receiver)
        await bot.send_message(chat_id=receiver, text=message.text)"""
