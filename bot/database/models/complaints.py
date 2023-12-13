

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from bot.database.database import Base, TimestampMixin


class Complaint(TimestampMixin, Base):
    
    client_id = mapped_column(ForeignKey('user.id'))
    manager_id = mapped_column(ForeignKey('user.id'))
    client: Mapped["User"] = relationship("User", foreign_keys=[client_id], back_populates="complaints_submitted")
    manager: Mapped["User"] = relationship("User", foreign_keys=[manager_id], back_populates="complaints_handled")
    
    # Параметры претензии
    invoice_id = mapped_column(ForeignKey('invoice.id'))
    email: Mapped[str]
    situation_description: Mapped[str]
    required_amount: Mapped[str]
    photo_scan: Mapped[str]