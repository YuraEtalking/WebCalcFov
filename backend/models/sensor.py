import math
from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from backend.core.db import Base
from backend.core.constants import FULL_FRAME_DIAGONAL
from backend.models.enums import SensorType
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    TimeFieldsMixin,
)


if TYPE_CHECKING:
    from .camera import Camera


class Sensor(IdMixin, ActiveMixin, Base, TimeFieldsMixin):
    """Модель датчика изображения."""
    sensor_type: Mapped[SensorType] = mapped_column(
        Enum(SensorType, name='sensor_type_enum'),
        nullable=False,
        default=SensorType.FULL_FRAME,
    )

    cameras: Mapped[list['Camera']] = relationship(
        back_populates='sensor',
        cascade='all, delete-orphan',
    )

    @property
    def width(self) -> float:
        return self.sensor_type.width

    @property
    def height(self) -> float:
        return self.sensor_type.height

    @property
    def crop_factor(self) -> float:
        diagonal = math.sqrt(self.width ** 2 + self.height ** 2)
        return FULL_FRAME_DIAGONAL / diagonal

    def __str__(self):
        return self.sensor_type.value

