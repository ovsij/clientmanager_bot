from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from bot.database.database import *
from bot.keyboards import *
from bot.utils.states import SendMessage


admin_callbacks_router = Router()

@admin_callbacks_router.callback_query(lambda c: c.data.startswith('admin'))
async def admin_callback_query_handler(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    code = callback_query.data
    tg_id = str(callback_query.from_user.id)
    print('admin: ' + code)
    if code == 'admin_delete_msg':
        await state.clear()
        await callback_query.message.delete()
    if code == 'admin':
        await state.clear()
        text, reply_markup = inline_kb_admin(db_request)
        try:
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        except:
            await callback_query.message.delete()
            await callback_query.message.answer(text=text, reply_markup=reply_markup)
    if 'admin_sending' in code:
        if code == 'admin_sending':
            await state.set_state(Form.sending)
            text, reply_markup = inline_kb_sending()
            msg = await callback_query.message.answer(text=text, reply_markup=reply_markup)
            await state.update_data(message=msg)
        if 'accept' in code:
            data = await state.get_data()
            if 'all' in code:
                users = db_request.get_user()
            elif 'new' in code:
                users = db_request.get_user(date='week')

            for user in users:
                try:
                    await bot.send_message(chat_id=user.tg_id, text=data['text'])
                except:
                    pass

            await callback_query.message.answer(text=data['text'] + '\n\nСообщение отправлено', reply_markup=InlineConstructor.create_kb(text_and_data=[['Скрыть', 'delete_msg']]))
            await callback_query.message.delete()
    