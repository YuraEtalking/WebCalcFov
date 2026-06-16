from datetime import datetime, date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Date, Enum, Integer, String, func

from starlette.requests import Request

from backend.core.constants.constants import MANUFACTURER_MAX_LEN, NAME_MAX_LEN
from backend.models.enums import BayonetType

class IdMixin:
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


class ManufacturerFieldsMixin:
    """Поле производителя."""
    manufacturer: Mapped[str] = mapped_column(
        String(MANUFACTURER_MAX_LEN),
        nullable=False,
    )


class NameFieldsMixin:
    """Поле имени объекта."""
    name: Mapped[str] = mapped_column(
        String(NAME_MAX_LEN),
        unique=True,
        nullable=False,
    )

class CommonFieldsMixin(ManufacturerFieldsMixin, NameFieldsMixin):
    """Общие поля."""
    pass


class ProductionPeriodMixin:
    """Даты начала и окончания производства"""
    production_start_date: Mapped[date] = mapped_column(Date, nullable=True)
    production_end_date: Mapped[date] = mapped_column(Date, nullable=True)


class BayonetMixin:
    """Тип байонета."""
    bayonet: Mapped[BayonetType] = mapped_column(
        Enum(BayonetType, name='bayonet_type_enum'),
        nullable=False,
    )


class AdminReprMixin:
    """Миксин для стандартного отображения моделей в админке.

    По умолчанию использует поле `name`.
    Чтобы переопределить, задайте `__admin_repr_field__` в модели.
    Поддерживает вложенные поля связанных моделей 'lens.name'.
    """
    __admin_repr_field__: str = 'name'

    def _get_admin_repr_value(self) -> str:
        value = self

        for field in self.__admin_repr_field__.split('.'):
            value = getattr(value, field, None)
            if value is None:
                return ''

        return str(value)

    async def __admin_repr__(self, request: Request) -> str:
        return self._get_admin_repr_value()

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f'<span>{self._get_admin_repr_value()}</span>'
