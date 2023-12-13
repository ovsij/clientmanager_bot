import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram import F

import os
import sys
from bot.database.database import get_async_session

from bot.utils.bot_commands import set_commands
from bot.utils.bot_description import set_bot_description
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from bot.config import config
from bot.middlewares.db_session import DbSessionMiddleware


logger = logging.getLogger(__name__)
#bot = Bot(token=config.bot.token, parse_mode='HTML', disable_web_page_preview=True)

async def on_startup(dispatcher: Dispatcher):
    config = dispatcher.workflow_data["config"]
    
    

    from bot import routers

    routers.register_all_routes(dispatcher, config)
    """from aiohttp import web
    from bot.routers.clients.webapp import app
    from aiogram.utils.web_app import WebAppInstance
    WebAppInstance.set_current(app)"""



# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting Bot')

    bot = Bot(token=config.bot.token, parse_mode='HTML', disable_web_page_preview=True)
    

    dp = Dispatcher()
    dp.workflow_data.update(
        config=config,
    )
    dp.update.middleware.register(DbSessionMiddleware(bot))

    await set_commands(bot)
    await set_bot_description(bot)

    dp.startup.register(on_startup)

    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        logging.warning("Bot polling is stopped.")
