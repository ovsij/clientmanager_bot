from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.keyboards.inline import *


clients_commands_router = Router()

@clients_commands_router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    text = inline_kb_welcome(first_name=message.from_user.first_name)
    await message.answer(text=text)
    await message.delete()

@clients_commands_router.message(Command(commands=["invoice"]))
async def cmd_invoice(message: Message, state: FSMContext):
    await state.clear()
    text, reply_markup = inline_kb_invoice()
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@clients_commands_router.message(Command(commands=["complaint"]))
async def cmd_invoice(message: Message, state: FSMContext):
    await state.clear()
    text, reply_markup = inline_kb_complaint()
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@clients_commands_router.message(Command(commands=["manager"]))
async def cmd_invoice(message: Message, state: FSMContext):
    await state.clear()
    text, reply_markup = inline_kb_manager()
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

