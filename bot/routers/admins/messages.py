from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.database import *
from bot.keyboards import *
from bot.keyboards.keyboard_constructor import InlineConstructor
from bot.utils.states import SendMessage

admin_messages_router = Router()


@admin_messages_router.message(SendMessage.sending)
async def get_sending(message: Message, state: FSMContext):
    pass
