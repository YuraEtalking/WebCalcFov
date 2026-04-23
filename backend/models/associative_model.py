from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean

from backend.core import Base

if TYPE_CHECKING:
    from .camera import Camera
    from .lens import Lens


class CameraLens(Base):
    __tablename__ = 'camera_lens'

    camera_id: Mapped[int] = mapped_column(
        ForeignKey('camera.id'),
        primary_key=True,
    )
    lens_id: Mapped[int] = mapped_column(
        ForeignKey('lens.id'),
        primary_key=True,
    )
    convertor: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    camera: Mapped['Camera'] = relationship(back_populates='camera_lenses')
    lens: Mapped['Lens'] = relationship(back_populates='camera_lenses')
