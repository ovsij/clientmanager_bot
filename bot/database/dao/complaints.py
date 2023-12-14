
from bot.database.dao.base import BaseDAO
from bot.database.dao.invoices import InvoiceDAO
from bot.database.dao.users import UserDAO
from bot.database.models.complaints import Complaint


class ComplaintDAO(BaseDAO):
    model = Complaint

    @classmethod
    async def add_one(cls, tg_id, data):
        client, manager = await UserDAO.get_clients_manager(client_tg_id=tg_id)
        data['client_id'] = client.id
        data['manager_id'] = manager.id
        
        invoice = await InvoiceDAO.get_one_or_none(id=data['invoice_id'])
        print(invoice)
        if not invoice:
            del data['invoice_id']
        print(data)
        complaint = await super().add_one(**data)
        print(complaint)
