from typing import Literal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.database import Base, TimestampMixin


class Invoice(TimestampMixin, Base):

    client_id = mapped_column(ForeignKey("user.id"))
    client: Mapped["User"] = relationship(
        "User", back_populates="invoices", lazy="select"
    )

    # Параметры накладной
    description: Mapped[str]
    weight: Mapped[float]
    dimensions: Mapped[str]
    pickup_address: Mapped[str]
    delivery_address: Mapped[str]
    payment_method: Mapped[str]

    def __str__(self):
        return f"Накладная №{self.id}"
