from aiohttp import web
from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
from pydantic import BaseModel

class UserData(BaseModel):
    last_name: str
    first_name: str
    middle_name: str

async def handle_form(request):
    data = await request.post()
    auth_data = data.get('_auth')  # Получаем данные из поля '_auth'

    bot = request.app['bot']
    try:
        webapp_data: WebAppInitData = safe_parse_webapp_init_data(
            token=bot.token, init_data=auth_data
        )
        user_data = UserData(**webapp_data.dict())  # Создаем объект UserData из данных WebAppInitData

        # Делаем что-то с полученными данными, например, отправляем сообщение в телеграм-чат
        chat_id = webapp_data.query_id
        await bot.send_message(chat_id, f"Last Name: {user_data.last_name}, First Name: {user_data.first_name}, Middle Name: {user_data.middle_name}")

        return web.json_response({"ok": True, "message": "Data received and processed successfully"})
    except ValueError:
        return web.json_response({"ok": False, "error": "Unauthorized"}, status=401)

app = web.Application()
app.router.add_post('/submit', handle_form)  # Эндпоинт для обработки POST запросов на /submit

