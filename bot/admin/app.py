import re

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi_storages import FileSystemStorage
from sqladmin import Admin, ModelView
from sqlalchemy import select

from bot.database.database import async_session_maker, engine
from bot.database.models.complaints import Complaint
from bot.database.models.invoices import Invoice
from bot.database.models.users import User

app = FastAPI()
admin = Admin(app, engine)
storage = FileSystemStorage(path="/tmp")


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_list = [User.id, User.manager_id] + [
        c.name for c in User.__table__.c if c.name not in ["id", "manager_id"]
    ]
    column_searchable_list = [
        User.id,
        User.username,
        User.first_name,
        User.last_name,
        User.tg_id,
    ]
    column_default_sort = [("is_manager", True), ("id", False)]
    page_size = 50
    page_size_options = [25, 50, 100, 200]


class InvoiceAdmin(ModelView, model=Invoice):
    name = "Накладная"
    name_plural = "Накладные"
    icon = "fa-solid fa-truck"
    column_list = [Invoice.id] + [c.name for c in Invoice.__table__.c if c.name != "id"]
    page_size = 50
    page_size_options = [25, 50, 100, 200]


class ComplaintAdmin(ModelView, model=Complaint):
    name = "Жалоба"
    name_plural = "Жалобы"
    icon = "fa-solid fa-bug"
    column_list = [Complaint.id] + [
        c.name for c in Complaint.__table__.c if c.name != "id"
    ]
    column_formatters = {
        Complaint.photo_scan: lambda m, a: re.findall(
            r'"([^"]*)"', "".join(m.photo_scan)
        )
    }
    column_formatters_detail = {
        Complaint.photo_scan: lambda m, a: re.findall(
            r'"([^"]*)"', "".join(m.photo_scan)
        )
    }
    page_size = 50
    page_size_options = [25, 50, 100, 200]


admin.add_view(UserAdmin)
admin.add_view(InvoiceAdmin)
admin.add_view(ComplaintAdmin)


@app.get("/get_photo/{photo_name}")
async def get_photo(photo_name: str) -> FileResponse:
    directory = "bot/database/photos"

    # Путь к запрошенной фотографии
    file_path = f"{directory}/{photo_name}"

    # Отправляем фотографию в ответе
    return FileResponse(file_path)
