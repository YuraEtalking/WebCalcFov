from typing import TYPE_CHECKING

from sqlalchemy import Enum, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
)
from backend.models.enums import ConstructionType

if TYPE_CHECKING:
    from .camera import Camera
    from .associative_model import CameraLens
    from .teleconverter import Teleconverter


class Lens(
    IdMixin,
    ActiveMixin,
    Base,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
):
    camera_lenses: Mapped[list['CameraLens']] = relationship(
        back_populates='lens',
        cascade='all, delete-orphan',
    )
    compatible_cameras: Mapped[list['Camera']] = relationship(
        secondary='camera_lens',
        viewonly=True,
    )
    type_lens: Mapped[ConstructionType] = mapped_column(
        Enum(ConstructionType,
        name='construction_type_enum'),
        nullable=False,
        default=ConstructionType.PRIME,
    )
    teleconverters: Mapped[list['Teleconverter']] = relationship(
        secondary='lens_teleconverter',
        back_populates='lenses',
        order_by='Teleconverter.multiplier',
    )

    focal_min: Mapped[int] = mapped_column(Integer, nullable=True)
    focal_max: Mapped[int] = mapped_column(Integer)

    aperture_min: Mapped[float] = mapped_column(Float, nullable=True)
    aperture_max: Mapped[float] = mapped_column(Float)

    def __str__(self):
        return self.name
