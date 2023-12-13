from datetime import datetime
import logging
from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware, Bot, types
from aiogram.types import Update, CallbackQuery, Message

from bot.config import config
from bot.database.dao.users import UserDAO
from bot.database.database import get_async_session
from bot.utils.bot_commands import set_commands


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    
    async def __call__(self,
                       handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
                       event: Union[Message, CallbackQuery],
                       data: Dict[str, Any],
                       ) -> Any:
        msg_text = None
        if event.message:
            tg_user: types.User = event.message.from_user
            msg_text = event.message.text
        elif event.callback_query:
            tg_user: types.User = event.callback_query.from_user
        user = await UserDAO.get_one_or_none(tg_id=str(tg_user.id))
        data["user"] = user
        # register user if not exists
        if not user:
            manager = await UserDAO.get_free_manager()
            print(manager)
            if tg_user.id in config.bot.admin_ids:
                user = await UserDAO.add_one(
                    **{'tg_id': str(tg_user.id), 
                     'username': tg_user.username,
                     'first_name': tg_user.first_name,
                     'last_name': tg_user.last_name,
                     'is_admin': True,
                     'is_manager': True
                     }
                )
            else:
                user = await UserDAO.add_one(
                    **{'tg_id': str(tg_user.id), 
                     'username': tg_user.username,
                     'first_name': tg_user.first_name,
                     'last_name': tg_user.last_name,
                     'manager_id': manager.id
                     }
                )
            logging.info(f"new user {tg_user.id} ({tg_user.full_name}) in db")
            await set_commands(self.bot)
        # update user data if changed
        """try:
            if user.username != tg_user.username or \
                    user.first_name != tg_user.first_name or \
                    user.last_name != tg_user.last_name:
                UserDAO.update(tg_id=str(tg_user.id),
                                        updated_fields={
                                            "username": tg_user.username,
                                            "first_name": tg_user.first_name,
                                            "last_name": tg_user.last_name,
                                            "last_use": datetime.now()
                                        })
            else:
                pass
        except:
            pass"""
            
        return await handler(event, data)