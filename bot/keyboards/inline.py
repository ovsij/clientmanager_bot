from aiogram.utils.formatting import *

from bot.database.dao.users import UserDAO
from bot.keyboards.keyboard_constructor import InlineConstructor


def inline_kb_welcome(first_name: str):
    text = as_line(
        f"Добро пожаловать, {first_name}!",
        "",
        "Чтобы начать пользоваться ботом достаточно выбрать одну из команд в меню, которое открывается кнопкой в нижнем левом углу экрана.",
        "",
        "/invoice - 🟢 Добавить накладную",
        "/complaint - 🔴 Подать жалобу",
        "/manager - 👤 Связаться с менеджером",
        "",
        "Желаем хорошего дня!",
        sep="\n",
    )
    return text.as_html()


def inline_kb_invoice():
    text = as_line(
        "Для того, чтобы заполнить накладную, вам нужно будет прислать боту по очереди следующие данные:",
        "🔹 Описание груза",
        "🔹 Вес груза",
        "🔹 Габариты груза",
        "🔹 Точный адрес отправки",
        "🔹 Точный адрес получения",
        "🔹 Способ оплаты",
        sep="\n",
    )
    text_and_data = [["Приступить", "createinvoice"]]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup


def inline_kb_create_invoice(next_text: str, data: dict = {}):
    keys = list(data.keys())
    text = as_line(
        "Для того, чтобы заполнить накладную, вам нужно будет прислать боту по очереди следующие данные:"
    )
    text += as_line("🔹 Описание груза")
    if "description" in keys:
        text += as_line(data["description"])
    text += as_line("🔹 Вес груза")
    if "weight" in keys:
        text += as_line(data["weight"])
    text += as_line("🔹 Габариты груза")
    if "dimensions" in keys:
        text += as_line(data["dimensions"])
    text += as_line("🔹 Точный адрес отправки:")
    if "pickup_address" in keys:
        text += as_line(data["pickup_address"])
    text += as_line("🔹 Точный адрес получения:")
    if "delivery_address" in keys:
        text += as_line(data["delivery_address"])
    text += as_line("🔹 Способ оплаты:")
    if "payment" in keys:
        payment_rus = {"card": "картой", "cash": "наличными"}
        text += as_line(payment_rus[data["payment"]])
    text += as_line("", Bold(next_text), sep="\n")
    text_and_data = [
        ["Отмена", "deny"],
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup


def inline_kb_payment_method(text):
    text = text
    text_and_data = [
        ["Картой", "payment_card"],
        ["Наличными", "payment_cash"],
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text, reply_markup


def inline_kb_complaint():
    text = as_line(
        "Для того, чтобы оформить претензию, вам нужно будет прислать боту по очереди следующие данные:",
        "🔹 Номер накладной",
        "🔹 E-mail для ответа на претензию",
        "🔹 Описание ситуации",
        "🔹 Требуемая сумма",
        "🔹 Фото/сканы",
        sep="\n",
    )
    text_and_data = [["Приступить", "createcomplaint"]]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup


def inline_kb_create_complaint(next_text: str, data: dict = {}):
    keys = list(data.keys())
    text = as_line(
        "Для того, чтобы оформить претензию, вам нужно будет прислать боту по очереди следующие данные:"
    )
    text += as_line("🔹 Номер накладной")
    if "invoice_id" in keys:
        text += as_line(data["invoice_id"])
    text += as_line("🔹 E-mail для ответа на претензию")
    if "email" in keys:
        text += as_line(data["email"])
    text += as_line("🔹 Описание ситуации")
    if "situation_description" in keys:
        text += as_line(data["situation_description"])
    text += as_line("🔹 Требуемая сумма")
    if "required_amount" in keys:
        text += as_line(data["required_amount"])
    text += as_line("🔹 Фото/сканы")
    if "photo_scan" in keys:
        text += as_line(f"Добавлено {len(data['photo_scan'])} фото/скана")

    text += as_line("", Bold(next_text), sep="\n")
    text_and_data = [
        ["Отмена", "deny"],
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup


async def inline_kb_myclients(clients):
    text = "Выберите клиента, с которым хотите начать обмен сообщениями"
    text_and_data = []
    for id in clients:
        client = await UserDAO.get_by_id(model_id=id)
        text_and_data.append([f"Клиент №{client.id}", f"managerclient_{client.id}"])
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text, reply_markup
