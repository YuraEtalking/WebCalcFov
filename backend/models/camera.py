from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
    ProductionPeriodMixin,
)


if TYPE_CHECKING:
    from .lens import Lens
    from .associative_model import CameraLens
    from .link import Link
    from .specs.camera_spec import SpecCamera
    from .image import CameraImageLink


class Camera(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    Base,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
    ProductionPeriodMixin,
):
    camera_lenses: Mapped[list['CameraLens']] = relationship(
        back_populates='camera',
        cascade='all, delete-orphan',
    )
    compatible_lenses: Mapped[list['Lens']] = relationship(
        secondary='camera_lens',
        viewonly=True,
    )

    links: Mapped[list['Link']] = relationship(
        secondary='link_camera',
        back_populates='cameras',
        order_by='Link.created_at',
    )
    spec: Mapped["SpecCamera | None"] = relationship(
        back_populates='camera',
        uselist=False,
        cascade='all, delete-orphan',
        single_parent=True,
    )
    image_links: Mapped[list['CameraImageLink']] = relationship(
        back_populates='camera',
        cascade='all, delete-orphan',
    )

    def __str__(self):
        return self.name

    @property
    def compatible_lenses_list(self) -> str:
        if not self.compatible_lenses:
            return '—'
        return ', '.join(lens.name for lens in self.compatible_lenses)
