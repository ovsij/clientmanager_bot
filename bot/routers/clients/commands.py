from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.keyboard_constructor import InlineConstructor

clients_commands_router = Router()

@clients_commands_router.message(Command(commands=["start"]))
async def add_command(message: Message):
    
    text_and_data = [['Открыть веб-приложение', 'https://rawcdn.githack.com/ovsij/clientmanager_bot/a5d3b9dd79a6cae63b4cd908ee10910a6b04fe30/bot/invoice_form.html']]
    reply_markup = InlineConstructor.create_kb(text_and_data, button_type=['web_app'])
    await message.answer("Чтобы добавить пользователя, нажмите кнопку ниже", reply_markup=reply_markup)
