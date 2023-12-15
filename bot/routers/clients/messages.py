import asyncio
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config import config
from bot.database.dao.chat import ChatDAO
from bot.database.dao.invoices import InvoiceDAO
from bot.keyboards.inline import (inline_kb_create_complaint,
                                  inline_kb_create_invoice,
                                  inline_kb_payment_method)
from bot.keyboards.keyboard_constructor import InlineConstructor
from bot.utils.states import ComplaintForm, InvoiceForm

clients_messages_router = Router()


@clients_messages_router.message(InvoiceForm.description)
async def get_description(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(description=message.text)
    await state.set_state(InvoiceForm.weight)
    data = await state.get_data()
    text, reply_markup = inline_kb_create_invoice(
        next_text="Пришлите вес груза в килограммах", data=data
    )
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(InvoiceForm.weight)
async def get_weight(message: Message, state: FSMContext):
    await message.delete()
    try:
        weight = float(message.text.replace(",", "."))
        await state.update_data(weight=weight)
        await state.set_state(InvoiceForm.dimensions)
        data = await state.get_data()
        text, reply_markup = inline_kb_create_invoice(
            next_text="Пришлите габариты груза", data=data
        )
        await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)
    except:
        data = await state.get_data()
        text, reply_markup = inline_kb_create_invoice(
            next_text="Пришлите сообщение с числом, равным весу груза в килограммах, без указания единицы измерения и других символов.",
            data=data,
        )
        await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(InvoiceForm.dimensions)
async def get_dimensions(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(dimensions=message.text)
    await state.set_state(InvoiceForm.pickup_address)
    data = await state.get_data()
    text, reply_markup = inline_kb_create_invoice(
        next_text="Пришлите точный адрес отправки груза", data=data
    )
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(InvoiceForm.pickup_address)
async def get_pickup_address(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(pickup_address=message.text)
    await state.set_state(InvoiceForm.delivery_address)
    data = await state.get_data()
    text, reply_markup = inline_kb_create_invoice(
        next_text="Пришлите точный адрес получения груза", data=data
    )
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(InvoiceForm.delivery_address)
async def get_delivery_address(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(delivery_address=message.text)
    await state.set_state(InvoiceForm.payment_method)
    data = await state.get_data()
    text, _ = inline_kb_create_invoice(next_text="Выберите способ оплаты", data=data)
    text, reply_markup = inline_kb_payment_method(text=text)
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(ComplaintForm.invoice_id)
async def get_invoice_number(message: Message, state: FSMContext):
    await message.delete()
    """The invoice number mist be an integer"""
    try:
        invoice_id = int(message.text)
    except:
        data = await state.get_data()
        text, reply_markup = inline_kb_create_complaint(
            next_text="Пришлите номер накладной числом без дополнительных символов",
            data=data,
        )
        await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)
    """The invoice number must exist"""
    invoice = await InvoiceDAO.get_one_or_none(id=invoice_id)
    if invoice:
        await state.update_data(invoice_id=invoice_id)
        await state.set_state(ComplaintForm.email)
        data = await state.get_data()
        text, reply_markup = inline_kb_create_complaint(
            next_text="E-mail для ответа на претензию", data=data
        )
        await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)
    else:
        await state.update_data(invoice_id=invoice_id)
        data = await state.get_data()
        text, _ = inline_kb_create_complaint(
            next_text='Накладная с таким номером не найдена, попробуйте ввести другой номер или нажмите "Продолжить", чтобы оставить введенный вами номер.',
            data=data,
        )
        reply_markup = InlineConstructor.create_kb(
            [["Продолжить", "invioceid_continue"]]
        )
        await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(ComplaintForm.email)
async def get_email(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(email=message.text)
    await state.set_state(ComplaintForm.situation_description)
    data = await state.get_data()
    text, reply_markup = inline_kb_create_complaint(
        next_text="Пришлите описание ситуации", data=data
    )
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(ComplaintForm.situation_description)
async def get_situation_descriptionscription(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(situation_description=message.text)
    await state.set_state(ComplaintForm.required_amount)
    data = await state.get_data()
    text, reply_markup = inline_kb_create_complaint(
        next_text="Пришлите требуемую сумму в рублях", data=data
    )
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(ComplaintForm.required_amount)
async def get_description(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(required_amount=message.text)
    await state.set_state(ComplaintForm.photo_scan)
    data = await state.get_data()
    text, _ = inline_kb_create_complaint(
        next_text='Пришлите фото/сканы в одном сообщении (максимум 10 штук). После того как вы пришлете фото, нажмите "Продолжить"',
        data=data,
    )
    reply_markup = InlineConstructor.create_kb([["Продолжить", "photo_continue"]])
    await data["prev_msg"].edit_text(text=text, reply_markup=reply_markup)


@clients_messages_router.message(F.photo, ComplaintForm.photo_scan)
async def get_description(message: Message, state: FSMContext, bot: Bot):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    local_path = f"bot/database/photos/{datetime.now()}.jpg"
    await bot.download_file(file_path, local_path)
    data = await state.get_data()
    if "photo_scan" not in data:
        data["photo_scan"] = []

    photo = data["photo_scan"]
    photo.append(f'{config.bot.app_url}/get_photo/{local_path.split("/")[-1]}')
    await state.update_data(photo_scan=photo)
    await message.delete()


@clients_messages_router.message()
async def delete_messsage(message: Message, state: FSMContext, bot: Bot):
    users_in_open = await ChatDAO.get_users_in_open()
    if str(message.from_user.id) in users_in_open:
        receiver = await ChatDAO.get_receiver(tg_id=str(message.from_user.id))
        await bot.send_message(chat_id=receiver, text=message.text)
        return

    """Delete not handled messages"""
    await message.delete()
