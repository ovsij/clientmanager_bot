from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.database import *
from bot.keyboards import *

admin_commands_router = Router()


@admin_commands_router.message(Command("admin"))
async def cmd_admin(message: Message):
    text, reply_markup = inline_kb_admin(db_request)
    await message.answer(text=text, reply_markup=reply_markup)
