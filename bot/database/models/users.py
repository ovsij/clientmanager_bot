from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.database import Base, TimestampMixin


class User(TimestampMixin, Base):

    tg_id: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str | None] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_manager: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    
    # manager - client relation
    manager_id = mapped_column(ForeignKey('user.id'))
    clients: Mapped[list["User"]] = relationship("User", back_populates="manager", remote_side="User.manager_id")
    manager: Mapped["User"] = relationship("User", back_populates="clients", remote_side="User.id")
    invoices: Mapped[list["Invoice"]] = relationship("Invoice", back_populates="client")
    complaints_submitted: Mapped[list["Complaint"]] = relationship("Complaint", back_populates="client", primaryjoin="Complaint.client_id == User.id")
    complaints_handled: Mapped[list["Complaint"]] = relationship("Complaint", back_populates="manager", primaryjoin="Complaint.manager_id == User.id")

    def __str__(self):
        name = f'@{self.username}' if self.username else self.tg_id
        if self.is_manager:
            return f"Менеджер {self.id}. {name}"
        else:
            return f"Клиент {self.id}. {name}"