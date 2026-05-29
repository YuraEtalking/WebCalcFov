import math
from typing import TYPE_CHECKING

from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from starlette.requests import Request

from backend.core.db import Base
from backend.core.constants import FULL_FRAME_DIAGONAL
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
    CommonFieldsMixin,
)


if TYPE_CHECKING:
    from .camera import Camera


class Sensor(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    Base,
    TimeFieldsMixin,
    CommonFieldsMixin,
):
    """Модель датчика изображения."""
    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)

    cameras: Mapped[list['Camera']] = relationship(
        back_populates='sensor',
        cascade='all, delete-orphan',
    )

    @property
    def crop_factor(self) -> float:
        diagonal = math.sqrt(self.width ** 2 + self.height ** 2)
        return FULL_FRAME_DIAGONAL / diagonal

    def __str__(self):
        return (f'{self.name} - '
                f'{self.width} х {self.height} мм')
