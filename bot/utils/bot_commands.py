from aiogram import Bot
from aiogram.types import (BotCommand, BotCommandScopeAllPrivateChats,
                           BotCommandScopeChat, BotCommandScopeDefault)
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Config
from bot.database.dao import UserDAO


async def set_commands(bot: Bot,) -> None:
    pass
