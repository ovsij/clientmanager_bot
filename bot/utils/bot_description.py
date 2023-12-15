from aiogram import Bot


async def set_bot_description(bot: Bot):
    description = "Что умеет делать этот бот?\nClientManagerBot поможет вам наладить взаимодействие клиентов вашего предприятия с менеджерами. \nВ настоящий момент реализован функционал добавления накладной, жалобы, а так же чата между клиентом и закрепенным за ним менеджером."
    await bot.set_my_description(description=description)
