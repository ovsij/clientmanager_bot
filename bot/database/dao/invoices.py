from bot.database.dao.base import BaseDAO
from bot.database.dao.users import UserDAO
from bot.database.models.invoices import Invoice


class InvoiceDAO(BaseDAO):
    model = Invoice

    @classmethod
    async def add_one(cls, tg_id: str, data):
        client = await UserDAO.get_one_or_none(tg_id=tg_id)
        if client:
            data["client_id"] = client.id
        invoice = await super().add_one(**data)
        return invoice
