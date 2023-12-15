from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from bot.database.dao.chat import ChatDAO

from bot.database.dao.complaints import ComplaintDAO
from bot.database.dao.invoices import InvoiceDAO
from bot.database.dao.users import UserDAO
from bot.keyboards.inline import (inline_kb_create_complaint,
                                  inline_kb_create_invoice)
from bot.utils.check_poll_completion import check_poll_completion
from bot.utils.states import ComplaintForm, InvoiceForm

clients_callbacks_router = Router()


@clients_callbacks_router.callback_query()
async def callback_query_handler(
    callback_query: types.CallbackQuery, state: FSMContext, bot: Bot
):
    code = callback_query.data
    tg_id = str(callback_query.from_user.id)
    print(f"{callback_query.from_user.username}[{tg_id}]: {code}")
    if code == "deny":
        await state.clear()
        await callback_query.message.delete()

    """Invoice callbacks"""
    if code == "createinvoice":
        await state.set_state(InvoiceForm.description)
        await state.update_data(not_finished=True)
        text, reply_markup = inline_kb_create_invoice(
            next_text="Пришлите описание груза"
        )
        msg = await callback_query.message.edit_text(
            text=text, reply_markup=reply_markup
        )
        await state.update_data(prev_msg=msg)
        await check_poll_completion(type="invoice", tg_id=tg_id, bot=bot, state=state)
    if code.startswith("payment"):
        await state.update_data(payment_method=code.split("_")[1])
        data = await state.get_data()
        text, _ = inline_kb_create_invoice(
            next_text="Накладная готова, сейчас пришлем pdf", data=data
        )
        await data["prev_msg"].edit_text(text=text)
        del data["not_finished"]
        del data["prev_msg"]
        await InvoiceDAO.add_one(tg_id=tg_id, data=data)
        await state.clear()

    """Complaint callbacks"""
    if code == "createcomplaint":
        await state.set_state(ComplaintForm.invoice_id)
        await state.update_data(not_finished=True)
        text, reply_markup = inline_kb_create_complaint(
            next_text="Пришлите номер накладной"
        )
        msg = await callback_query.message.edit_text(
            text=text, reply_markup=reply_markup
        )
        await state.update_data(prev_msg=msg)
        await check_poll_completion(type="complaint", tg_id=tg_id, bot=bot, state=state)
    if code == "invioceid_continue":
        await state.set_state(ComplaintForm.email)
        data = await state.get_data()
        text, reply_markup = inline_kb_create_complaint(
            next_text="Пришлите E-mail для ответа на претензию", data=data
        )
        await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)
    if code == "photo_continue":
        data = await state.get_data()

        text, _ = inline_kb_create_complaint(
            next_text="Претензия оформлена и направлена вашему менеджеру. Сейчас пришлем pdf.",
            data=data,
        )
        await data["prev_msg"].edit_text(text=text)
        del data["not_finished"]
        del data["prev_msg"]

        await ComplaintDAO.add_one(tg_id=tg_id, data=data)
        await state.clear()

    """Managers callbacks. Move it from here!!!"""
    if code.startswith("managerclient"):
        client_id = int(code.split("_")[-1])
        # client = await UserDAO.get_by_id(model_id=client_id)
        chat = await ChatDAO.update(
            client_id=client_id, manager_tg_id=tg_id, is_open=True
        )
        await callback_query.message.answer(
            "Диалог с клиентом открыт. Закрыть все диалоги - /close"
        )
