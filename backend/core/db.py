from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from backend.core.config import settings
from backend.core.constants import MANUFACTURER_MAX_LEN, NAME_MAX_LEN


class BaseModel:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

class TimeFieldsMixin:
    """Даты создания и обновления"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

class ActiveMixin:
    """Возможность скрывать из выдачи."""
    is_active = Column(Boolean, nullable=False, default=True)

class CommonFieldsMixin:
    """Общие поля для сущностей."""
    manufacturer = Column(String(MANUFACTURER_MAX_LEN), nullable=False)
    name = Column(String(NAME_MAX_LEN), unique=True, nullable=False)


Base = declarative_base(cls=BaseModel)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
