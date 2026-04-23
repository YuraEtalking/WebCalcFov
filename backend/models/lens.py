from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from backend.core import ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin
from backend.models import CameraLens


if TYPE_CHECKING:
    from .associative_model import CameraLens


class Lens(ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin):
    camera_lenses: Mapped[list['CameraLens']] = relationship(
        back_populates='lens',
        cascade='all, delete-orphan',
    )