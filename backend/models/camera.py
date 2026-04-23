from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from backend.core import ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin


if TYPE_CHECKING:
    from .associative_model import CameraLens


class Camera(ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin):
    camera_lenses: Mapped[list['CameraLens']] = relationship(
        back_populates='camera',
        cascade='all, delete-orphan',
    )

    # TODO подумай над полями, может оформить отдельные странички с доп инфой.