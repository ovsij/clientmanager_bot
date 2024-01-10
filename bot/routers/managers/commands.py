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
    pass


@managers_commands_router.message(Command(commands=["close"]))
async def cmd_myclients(message: Message, state: FSMContext):
    pass
