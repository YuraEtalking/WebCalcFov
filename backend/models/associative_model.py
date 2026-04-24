from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey

from backend.core.db import Base
from backend.models.enums import CompatibilityType

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
    convertor: Mapped[CompatibilityType] = mapped_column(
        Enum(CompatibilityType,
        name='compatibility_type_enum'),
        nullable=False,
        default=CompatibilityType.DIRECT,
    )
    camera: Mapped['Camera'] = relationship(back_populates='camera_lenses')
    lens: Mapped['Lens'] = relationship(back_populates='camera_lenses')

    def __str__(self):
        return f'Камера ID: {self.camera_id}, Объектив ID: {self.lens_id}'
