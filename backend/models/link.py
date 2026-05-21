from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
)


if TYPE_CHECKING:
    from .camera import Camera
    from .lens import Lens
    from .teleconverter import Teleconverter
    from .sensor import Sensor



class Link(
    IdMixin,
    ActiveMixin,
    Base,
    TimeFieldsMixin,
):
    """Модель ссылок на обзоры/тесты/статьи."""
    cameras: Mapped[list['Camera']] = relationship(
        secondary='link_camera',
        back_populates='links',
    )

    lenses: Mapped[list['Lens']] = relationship(
        secondary='link_lens',
        back_populates='links',
    )

    teleconverters: Mapped[list['Teleconverter']] = relationship(
        secondary='link_teleconverter',
        back_populates='links',
    )

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )

    def __str__(self):
        return self.title
