from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.database.database import Base, TimestampMixin


class Chat(TimestampMixin, Base):
    client_id = mapped_column(ForeignKey("user.id"))
    manager_id = mapped_column(ForeignKey("user.id"))
    client: Mapped["User"] = relationship(
        "User", foreign_keys=[client_id], back_populates="chat_submitted"
    )
    manager: Mapped["User"] = relationship(
        "User", foreign_keys=[manager_id], back_populates="chat_handled"
    )

    is_open: Mapped[bool] = mapped_column(default=False)
    is_archived: Mapped[bool] = mapped_column(default=False)
