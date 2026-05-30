from typing import TYPE_CHECKING

from sqlalchemy import Enum, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
)


if TYPE_CHECKING:
    from .camera import Camera
    from .associative_model import CameraLens
    from .teleconverter import Teleconverter
    from .link import Link
    from models.specs.lens_spec import SpecLens


class Lens(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
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
    teleconverters: Mapped[list['Teleconverter']] = relationship(
        secondary='lens_teleconverter',
        back_populates='lenses',
        order_by='Teleconverter.multiplier',
    )
    links: Mapped[list['Link']] = relationship(
        secondary='link_lens',
        back_populates='lenses',
        order_by='Link.created_at',
    )
    spec: Mapped["SpecLens | None"] = relationship(
        back_populates='lens',
        uselist=False,
        cascade='all, delete-orphan',
        single_parent=True,
    )

    focal_wide: Mapped[int] = mapped_column(Integer, nullable=True)
    focal_tele: Mapped[int] = mapped_column(Integer)

    aperture_max_wide: Mapped[float] = mapped_column(Float, nullable=True)
    aperture_max_tele: Mapped[float] = mapped_column(Float)

    def __str__(self):
        return self.name
