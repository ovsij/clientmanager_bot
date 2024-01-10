from bot.database.dao.base import BaseDAO
from bot.database.dao.invoices import InvoiceDAO
from bot.database.dao.users import UserDAO
from bot.database.models.claims import Claim


class ClaimDAO(BaseDAO):
    model = Claim

    @classmethod
    async def add_one(cls, tg_id, data):
        pass
