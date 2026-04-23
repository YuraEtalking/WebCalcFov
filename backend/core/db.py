from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Enum, Integer, String, func
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declared_attr

from backend.core.config import settings
from backend.core.constants import MANUFACTURER_MAX_LEN, NAME_MAX_LEN
from backend.models.enums import BayonetType

class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class TimeFieldsMixin:
    """Даты создания и обновления"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

class ActiveMixin:
    """Возможность скрывать из выдачи."""
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

class CommonFieldsMixin:
    """Общие поля для сущностей."""
    manufacturer: Mapped[str] = mapped_column(
        String(MANUFACTURER_MAX_LEN),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LEN),
        unique=True,
        nullable=False,
    )

class BayonetMixin:
    bayonet: Mapped[BayonetType] = mapped_column(
        Enum(BayonetType, name='bayonet_type_enum', nullable=False)
    )


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as async_session:
        yield async_session
