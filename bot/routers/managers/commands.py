from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.dao.chat import ChatDAO
from bot.database.dao.users import UserDAO
from bot.keyboards.inline import inline_kb_myclients

managers_commands_router = Router()


@managers_commands_router.message(Command(commands=["myclients"]))
async def cmd_myclients(message: Message, state: FSMContext):
    await state.clear()
    chats = await ChatDAO.get_not_archived(manager_tg_id=str(message.from_user.id))
    text, reply_markup = await inline_kb_myclients(clients=chats)
    await message.answer(text=text, reply_markup=reply_markup)


@managers_commands_router.message(Command(commands=["close"]))
async def cmd_myclients(message: Message, state: FSMContext):
    await state.clear()
    manager = await UserDAO.get_one_or_none(tg_id=str(message.from_user.id))
    chat = await ChatDAO.get_one_or_none(manager_id=manager.id, is_open=True)
    await ChatDAO.update(
        manager_tg_id=str(message.from_user.id), client_id=chat.client_id, is_open=False
    )
    await message.answer("Чат с пользователем закрыт")
