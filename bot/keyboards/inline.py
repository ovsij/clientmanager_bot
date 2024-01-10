from aiogram.utils.formatting import *

from bot.database.dao.users import UserDAO
from bot.keyboards.keyboard_constructor import InlineConstructor


def inline_kb_welcome(first_name: str):
    pass


def inline_kb_invoice():
    pass


def inline_kb_create_invoice(next_text: str, data: dict = {}):
    pass


def inline_kb_payment_method(text):
    pass


def inline_kb_complaint():
    pass


def inline_kb_create_complaint(next_text: str, data: dict = {}):
    pass


async def inline_kb_myclients(clients):
    pass
