import re
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (Mapped, declarative_base, declared_attr,
                            mapped_column, sessionmaker)

from bot.config import config
from bot.utils.utils import get_local_ip


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)


Base = declarative_base(cls=CustomBase)

    
host = 'localhost' if get_local_ip() == config.postgres.host else config.postgres.host
DB_URL = f'postgresql+asyncpg://{config.postgres.user}:{config.postgres.password}@{host}:{config.postgres.port}/{config.postgres.database}'
engine = create_async_engine(DB_URL)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class TimestampMixin:
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    