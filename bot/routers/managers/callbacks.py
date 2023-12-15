from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from bot.database.dao.chat import ChatDAO

managers_callbacks_router = Router()


@managers_callbacks_router.callback_query()
async def callback_query_handler(
    callback_query: types.CallbackQuery, state: FSMContext, bot: Bot
):
    code = callback_query.data
    tg_id = str(callback_query.from_user.id)
    print(f"manager {callback_query.from_user.username}[{tg_id}]: {code}")

    if code.startswith("client"):
        client_id = int(code.split("_")[-1])
        # client = await UserDAO.get_by_id(model_id=client_id)
        chat = await ChatDAO.update(
            client_id=client_id, manager_tg_id=tg_id, is_open=True
        )
        await callback_query.message.answer(
            "Диалог с клиентом открыт. Закрыть все диалоги - /close"
        )
