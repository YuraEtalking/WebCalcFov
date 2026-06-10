from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Enum, Integer, String, func

from starlette.requests import Request

from backend.core.constants.constants import MANUFACTURER_MAX_LEN, NAME_MAX_LEN
from backend.models.enums import BayonetType


class WeightMixin:
    """Вес."""
    weight_g: Mapped[int | None] = mapped_column(Integer, nullable=True)

class WidthMixin:
    """Ширина."""
    width_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)

class HeightMixin:
    """Высота."""
    height_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)

class LengthMixin:
    """Длинна."""
    length_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)

class DiameterMixin:
    """Диаметр."""
    diameter_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)


class LensPhysicalSpecMixin(WeightMixin, DiameterMixin, LengthMixin):
    """Физические характеристики объектива"""
    pass

class CameraPhysicalSpecMixin(
    WeightMixin,
    WidthMixin,
    LengthMixin,
    HeightMixin
):
    """Физические характеристики камеры"""
    pass