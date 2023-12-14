from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import *
import asyncio

from bot.database.dao.users import UserDAO



async def check_poll_completion(type, tg_id, bot, state: FSMContext):
    await asyncio.sleep(30)
    type_rus = {'invoice': 'накладную', 'complaint' : 'жалобу'}
    data = await state.get_data()
    if 'not_finished' in list(data.keys()):
        client, manager = await UserDAO.get_clients_manager(client_tg_id=tg_id)
        name = (as_line(TextLink(f'@{client.username}', url=f't.me/{client.username}')) if \
            client.username else as_line(TextLink(f'{tg_id}', url=f'tg://user?id={tg_id}'))).as_html()
        await bot.send_message(chat_id=manager.tg_id, text=f'Пользователь №{client.id} {name} начал заполнять {type_rus[type]} и не закончил до конца.')
    else:
        pass