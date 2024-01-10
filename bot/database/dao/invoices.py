from bot.database.dao.base import BaseDAO
from bot.database.dao.users import UserDAO
from bot.database.models.invoices import Invoice


class InvoiceDAO(BaseDAO):
    model = Invoice

    @classmethod
    async def add_one(cls, tg_id: str, data):
        pass
