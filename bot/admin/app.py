from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import select

from bot.database.database import engine, async_session_maker
from bot.database.models.complaints import Complaint
from bot.database.models.invoice import Invoice
from bot.database.models.users import User

app = FastAPI()
admin = Admin(app, engine)

class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_list = [User.id, User.manager_id] + [c.name for c in User.__table__.c if c.name not in ['id', 'manager_id']]
    #[User.id, User.tg_id, User.username, User.first_name, User.last_name, User.is_admin, User.is_manager, User.is_active, User.manager_id]
    can_delete = False
    column_searchable_list = [User.id, User.username, User.first_name, User.last_name, User.tg_id]
    column_default_sort = [('is_manager', True), ('id', False)]
    page_size = 50
    page_size_options = [25, 50, 100, 200]

class InvoiceAdmin(ModelView, model=Invoice):
    column_list = "__all__"#[c.name for c in Invoice.__table__.c]
    #[User.id, User.tg_id, User.username, User.first_name, User.last_name, User.is_admin, User.is_manager, User.is_active, User.manager_id]
    page_size = 50
    page_size_options = [25, 50, 100, 200]

class ComplaintAdmin(ModelView, model=Complaint):
    column_list = "__all__"#[c.name for c in Complaint.__table__.c]
    #[User.id, User.tg_id, User.username, User.first_name, User.last_name, User.is_admin, User.is_manager, User.is_active, User.manager_id]
    page_size = 50
    page_size_options = [25, 50, 100, 200]

admin.add_view(UserAdmin)
admin.add_view(InvoiceAdmin)
admin.add_view(ComplaintAdmin)