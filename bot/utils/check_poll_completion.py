import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import *

from bot.database.dao.users import UserDAO


async def check_poll_completion(type, tg_id, bot, state: FSMContext):
    pass
