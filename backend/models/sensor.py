import math
from typing import TYPE_CHECKING

from sqlalchemy import Float, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base
from backend.core.constants.sensor_constants import FULL_FRAME_DIAGONAL
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
    CommonFieldsMixin,
)
from backend.models.enums import SensorFormat


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
    # cameras: Mapped[list['Camera']] = relationship(
    #     back_populates='sensor',
    #     cascade='all, delete-orphan',
    # )
    #
    # sensor_format: Mapped[SensorFormat] = mapped_column(
    #     Enum(SensorFormat, name='sensor_format_enum'),
    #     nullable=False,
    #     default=SensorFormat.FULL_FRAME,
    # )

    # width: Mapped[float] = mapped_column(Float)
    # height: Mapped[float] = mapped_column(Float)
    #
    # @property
    # def crop_factor(self) -> float:
    #     diagonal = math.sqrt(self.width ** 2 + self.height ** 2)
    #     return FULL_FRAME_DIAGONAL / diagonal
    #
    # def __str__(self):
    #     return (f'{self.name} - '
    #             f'{self.width} х {self.height} мм')
