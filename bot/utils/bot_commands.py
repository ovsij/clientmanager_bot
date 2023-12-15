from aiogram import Bot
from aiogram.types import (BotCommand, BotCommandScopeAllPrivateChats,
                           BotCommandScopeChat, BotCommandScopeDefault)
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import Config
from bot.database.dao import UserDAO


async def set_commands(bot: Bot,) -> None:
    commands = [
        BotCommand(command="invoice", description="🟢 Добавить накладную"),
        BotCommand(command="complaint", description="🔴 Подать жалобу"),
        BotCommand(command="manager", description="👤 Связаться с менеджером"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())

    managers = await UserDAO.get_all(is_manager=True)
    if managers:
        for manager in managers:
            try:
                commands.append(
                    BotCommand(command="myclients", description="🗣 Чаты с клиентами")
                )
                commands.append(
                    BotCommand(command="close", description="Закрыть чат с клиентом")
                )
                await bot.set_my_commands(
                    commands=commands, scope=BotCommandScopeChat(chat_id=manager.tg_id)
                )
            except:
                print(f"Command not created for: {manager}")
    admins = await UserDAO.get_all(is_admin=True)
    if admins:
        for admin in admins:
            try:
                commands.append(
                    BotCommand(command="admin", description="🥷 Меню администратора")
                )
                await bot.set_my_commands(
                    commands=commands, scope=BotCommandScopeChat(chat_id=admin.tg_id)
                )
            except:
                print(f"Command not created for: {admin}")
