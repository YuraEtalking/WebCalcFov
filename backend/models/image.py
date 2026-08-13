import enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Enum, Integer, String
from sqlalchemy_file import ImageField
from sqlalchemy.orm import Mapped, mapped_column, relationship


from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
)
if TYPE_CHECKING:
    from models.lens import Lens
    from .camera import Camera
    from .teleconverter import Teleconverter


class ImageRole(str, enum.Enum):
    photo = 'photo'
    mtf = 'mtf'
    chart = 'chart'
    sample = 'sample'
    scheme = 'scheme'


class ImageRoleMixin:
    role: Mapped[ImageRole] = mapped_column(
        Enum(ImageRole),
        index=True,
    )


class Image(
    Base,
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
):
    __admin_repr_field__ = 'title'

    # Основное
    file: Mapped[dict] = mapped_column(ImageField(
        upload_storage='images',
        thumbnail_size=(200, 200)
    ))  #  Alembic не добавляет импорт в миграцию, import sqlalchemy_file

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    alt: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Данные Exif
    photographer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    iso: Mapped[int] = mapped_column(Integer, nullable=True)
    shutter_speed: Mapped[str | None] = mapped_column(String(50), nullable=True)
    aperture: Mapped[str | None] = mapped_column(String(20), nullable=True)
    focal_length: Mapped[str | None] = mapped_column(String(20), nullable=True)
    camera_model_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lens_model_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    lens_links: Mapped[list['LensImageLink']] = relationship(
        back_populates='image',
        cascade='all, delete-orphan',
    )
    camera_links: Mapped[list['CameraImageLink']] = relationship(
        back_populates='image',
        cascade='all, delete-orphan',
    )
    teleconverter_links: Mapped[list['TeleconverterImageLink']] = relationship(
        back_populates='image',
        cascade='all, delete-orphan',
    )

    def __str__(self):
        return self.title or ''


class LensImageLink(
    Base,
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
    ImageRoleMixin,
):
    __tablename__ = 'lens_image_link'
    __admin_repr_field__ = 'lens.name'

    # ImageRoleMixin добавляет поле role

    lens_id: Mapped[int] = mapped_column(
        ForeignKey('lens.id', ondelete='CASCADE'),
        index=True,
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey('image.id', ondelete='CASCADE'),
        index=True,
    )

    lens: Mapped['Lens'] = relationship(back_populates='image_links')
    image: Mapped['Image'] = relationship(back_populates='lens_links')



class CameraImageLink(
    Base,
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
    ImageRoleMixin,
):
    __tablename__ = 'camera_image_link'

    # ImageRoleMixin добавляет поле role

    camera_id: Mapped[int] = mapped_column(
        ForeignKey('camera.id', ondelete='CASCADE'),
        index=True,
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey('image.id', ondelete='CASCADE'),
        index=True,
    )

    camera: Mapped['Camera'] = relationship(back_populates='image_links')
    image: Mapped['Image'] = relationship(back_populates='camera_links')


class TeleconverterImageLink(
    Base,
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
    ImageRoleMixin,
):
    __tablename__ = 'teleconverter_image_link'

    # ImageRoleMixin добавляет поле role

    teleconverter_id: Mapped[int] = mapped_column(
        ForeignKey('teleconverter.id', ondelete='CASCADE'),
        index=True,
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey('image.id', ondelete='CASCADE'),
        index=True,
    )

    teleconverter: Mapped['Teleconverter'] = relationship(
        back_populates='image_links'
    )
    image: Mapped['Image'] = relationship(back_populates='teleconverter_links')
