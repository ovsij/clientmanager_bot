from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from bot.database.database import *
from bot.keyboards import *
from bot.utils.states import SendMessage

admin_callbacks_router = Router()


@admin_callbacks_router.callback_query(lambda c: c.data.startswith("admin"))
async def admin_callback_query_handler(
    callback_query: types.CallbackQuery, state: FSMContext, bot: Bot
):
    pass
