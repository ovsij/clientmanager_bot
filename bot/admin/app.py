import re

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi_storages import FileSystemStorage
from sqladmin import Admin, ModelView
from sqlalchemy import select

from bot.database.database import async_session_maker, engine
from bot.database.models.claims import Claim
from bot.database.models.invoices import Invoice
from bot.database.models.users import User

app = FastAPI()
admin = Admin(app, engine)
storage = FileSystemStorage(path="/tmp")


class UserAdmin(ModelView, model=User):
    pass


class InvoiceAdmin(ModelView, model=Invoice):
    pass


class ClaimAdmin(ModelView, model=Claim):
    pass


admin.add_view(UserAdmin)
admin.add_view(InvoiceAdmin)
admin.add_view(ClaimAdmin)


@app.get("/get_photo/{photo_name}")
async def get_photo(photo_name: str) -> FileResponse:
    pass
