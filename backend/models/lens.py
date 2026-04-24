from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from backend.core.db import Base
from backend.models.mixins import (
    ActiveMixin,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
)

if TYPE_CHECKING:
    from .associative_model import CameraLens


class Lens(
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