from aiogram import Router
from aiogram.types import Message


clients_messages_router = Router()

@clients_messages_router.message()
async def x(message: Message):
    print(message)