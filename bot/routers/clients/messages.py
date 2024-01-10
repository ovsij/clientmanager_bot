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
from bot.utils.states import ClaimForm, InvoiceForm

clients_messages_router = Router()


@clients_messages_router.message(InvoiceForm.description)
async def get_description(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(InvoiceForm.weight)
async def get_weight(message: Message, state: FSMContext):
    await message.delete()
    pass


@clients_messages_router.message(InvoiceForm.dimensions)
async def get_dimensions(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(InvoiceForm.pickup_address)
async def get_pickup_address(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(InvoiceForm.delivery_address)
async def get_delivery_address(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(ClaimForm.invoice_id)
async def get_invoice_number(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(ClaimForm.email)
async def get_email(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(ClaimForm.situation_description)
async def get_situation_descriptionscription(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(ClaimForm.required_amount)
async def get_description(message: Message, state: FSMContext):
    pass


@clients_messages_router.message(F.photo, ClaimForm.photo_scan)
async def get_description(message: Message, state: FSMContext, bot: Bot):
    pass


@clients_messages_router.message()
async def delete_messsage(message: Message, state: FSMContext, bot: Bot):
    pass
