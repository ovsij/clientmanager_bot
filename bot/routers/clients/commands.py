from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.dao.chat import ChatDAO
from bot.keyboards.inline import *

clients_commands_router = Router()


@clients_commands_router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    pass


@clients_commands_router.message(Command(commands=["invoice"]))
async def cmd_invoice(message: Message, state: FSMContext):
    pass


@clients_commands_router.message(Command(commands=["complaint"]))
async def cmd_invoice(message: Message, state: FSMContext):
    pass


@clients_commands_router.message(Command(commands=["manager"]))
async def cmd_invoice(message: Message, state: FSMContext):
    pass
