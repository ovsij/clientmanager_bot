from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.keyboards import *
from bot.keyboards.keyboard_constructor import InlineConstructor
from bot.utils.states import Form

admin_messages_router = Router()

@admin_messages_router.message(Form.sending)
async def get_sending(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()

    text_and_data = [
        ['✅ Отправить всем', 'admin_sending_accept_all'],
        ['✅ Отправить неактивным пользователям', 'admin_sending_accept_new'],
        ['❌ Отменить', 'admin_delete_msg']
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    await message.answer(text, reply_markup=reply_markup)
    await message.delete()
    await data['message'].delete()
    