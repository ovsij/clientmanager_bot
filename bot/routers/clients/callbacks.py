from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from bot.database.dao.chat import ChatDAO

from bot.database.dao.claims import ClaimDAO
from bot.database.dao.invoices import InvoiceDAO
from bot.database.dao.users import UserDAO
from bot.keyboards.inline import (inline_kb_create_complaint,
                                  inline_kb_create_invoice)
from bot.utils.check_poll_completion import check_poll_completion
from bot.utils.states import ClaimForm, InvoiceForm

clients_callbacks_router = Router()


@clients_callbacks_router.callback_query()
async def callback_query_handler(
    callback_query: types.CallbackQuery, state: FSMContext, bot: Bot
):
    pass
