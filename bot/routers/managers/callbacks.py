from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from bot.database.dao.chat import ChatDAO

managers_callbacks_router = Router()


@managers_callbacks_router.callback_query(F.callback_query.data.startswith('manager'))
async def callback_query_handler(
    callback_query: types.CallbackQuery, state: FSMContext, bot: Bot
):
    pass
