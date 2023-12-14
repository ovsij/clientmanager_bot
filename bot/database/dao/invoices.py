
from bot.database.dao.base import BaseDAO
from bot.database.models.invoice import Invoice


class InvoiceDAO(BaseDAO):
    model = Invoice
