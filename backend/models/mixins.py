from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Enum, String, func

from backend.core.constants import MANUFACTURER_MAX_LEN, NAME_MAX_LEN
from backend.models.enums import BayonetType


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
    """Тип байонета."""
    bayonet: Mapped[BayonetType] = mapped_column(
        Enum(BayonetType, name='bayonet_type_enum'),
        nullable=False,
    )
