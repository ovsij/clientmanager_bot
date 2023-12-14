from typing import Literal, get_args
from sqlalchemy import ForeignKey
from sqlalchemy.types import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.database import Base, TimestampMixin

PaymentMethod = Literal['cash', 'card', 'bank', 'check', 'e-payment', 'e-money']

class Invoice(TimestampMixin, Base):
    
    client_id = mapped_column(ForeignKey('user.id'))
    client: Mapped["User"] = relationship(back_populates="invoices")
    
    # Параметры накладной
    description = Mapped[str]
    weight = Mapped[str]
    dimensions = Mapped[str]
    pickup_address = Mapped[str]
    delivery_address = Mapped[str]
    payment_method: Mapped[PaymentMethod] = mapped_column(Enum(
        *get_args(PaymentMethod),
        name="payment_method",
        create_constraint=True,
        validate_strings=True,
    ))

    def __str__(self):
        name = f'@{self.client.username}' if self.client.username else self.client.tg_id
        return f"Накладная №{id} ({name})"