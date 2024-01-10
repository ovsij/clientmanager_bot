from aiogram.fsm.state import State, StatesGroup


class SendMessage(StatesGroup):
    sending = State()


class InvoiceForm(StatesGroup):
    description = State()
    weight = State()
    dimensions = State()
    pickup_address = State()
    delivery_address = State()
    payment_method = State()


class ClaimForm(StatesGroup):
    invoice_id = State()
    email = State()
    situation_description = State()
    required_amount = State()
    photo_scan = State()
