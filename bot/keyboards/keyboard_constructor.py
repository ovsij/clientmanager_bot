from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InlineConstructor:
    @staticmethod
    def create_kb(
        text_and_data: list, schema: list = None, button_type: list = None
    ) -> InlineKeyboardMarkup:
        pass